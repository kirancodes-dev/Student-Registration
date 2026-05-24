import logging
from datetime import datetime
from flask import (
    Flask, render_template, redirect, url_for,
    flash, request, session, abort, jsonify, g
)
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config
from models import db, bcrypt, Student, Admin, generate_student_id
from forms import RegistrationForm, LoginForm, AdminLoginForm, ProfileUpdateForm
from security import init_security, get_session_config
from auth import TokenManager, PasswordManager, token_required
from validators import EmailValidator, PasswordValidator, InputSanitizer
from audit import AuditLog, log_request_response

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Apply security session configuration
    app.config.update(get_session_config())

    # Trust proxy headers (e.g. localhost.run reverse proxy)
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

    # Extensions
    db.init_app(app)
    bcrypt.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please sign in to access that page.'
    login_manager.login_message_category = 'info'

    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
    )
    
    # Initialize security features (headers, CORS, etc.)
    init_security(app)

    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    logger = logging.getLogger(__name__)
    audit_logger = AuditLog.get_logger()

    # -----------------------------------------------------------------------
    # User loader – handles both Student and Admin sessions
    # -----------------------------------------------------------------------
    @login_manager.user_loader
    def load_user(user_id):
        if str(user_id).startswith('admin-'):
            admin_id = int(user_id.split('-')[1])
            return Admin.query.get(admin_id)
        return Student.query.get(int(user_id))
    
    # Request context setup for audit logging
    @app.before_request
    def before_request():
        """Setup request context including user tracking."""
        g.request_id = request.headers.get('X-Request-ID', str(__import__('uuid').uuid4()))
        if current_user.is_authenticated:
            g.user_id = current_user.id
        else:
            g.user_id = None

    # -----------------------------------------------------------------------
    # Context processors
    # -----------------------------------------------------------------------
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    # -----------------------------------------------------------------------
    # Public routes
    # -----------------------------------------------------------------------
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/courses')
    @login_required
    def courses():
        if isinstance(current_user, Admin):
            return redirect(url_for('admin_dashboard'))
        return render_template('courses.html')

    # -----------------------------------------------------------------------
    # Registration
    # -----------------------------------------------------------------------
    @app.route('/register', methods=['GET', 'POST'])
    @limiter.limit("10 per hour")
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        form = RegistrationForm()

        if form.validate_on_submit():
            try:
                # Generate a unique student ID (retry if collision)
                sid = generate_student_id()
                while Student.query.filter_by(student_id=sid).first():
                    sid = generate_student_id()

                student = Student(
                    student_id=sid,
                    first_name=form.first_name.data.strip(),
                    last_name=form.last_name.data.strip(),
                    dob=form.dob.data,
                    gender=form.gender.data,
                    email=form.email.data.lower().strip(),
                    phone=form.phone.data.strip(),
                    street=form.street.data.strip(),
                    city=form.city.data.strip(),
                    state=form.state.data.strip(),
                    zip_code=form.zip_code.data.strip(),
                    country=form.country.data.strip(),
                    high_school=form.high_school.data.strip(),
                    graduation_year=form.graduation_year.data,
                    major=form.major.data,
                    enrollment_type=form.enrollment_type.data,
                )
                student.set_password(form.password.data)

                db.session.add(student)
                db.session.commit()

                logger.info(f"New student registered: {student.email} | ID: {student.student_id}")
                audit_logger.log_data_change(
                    'CREATE',
                    'STUDENT',
                    str(student.id),
                    'SYSTEM',
                    new_values={'email': student.email, 'student_id': student.student_id}
                )
                
                session['new_student_id'] = student.student_id
                session['new_student_name'] = student.first_name
                return redirect(url_for('confirmation'))
            except Exception as e:
                logger.error(f"Registration error: {str(e)}")
                audit_logger.log_event(
                    'REGISTRATION_ERROR',
                    f'Failed to register student: {str(e)}',
                    severity='ERROR'
                )
                flash('An error occurred during registration. Please try again.', 'error')
                db.session.rollback()

        # Collect field-level errors to pass to JS multi-step form
        step_errors = {1: False, 2: False, 3: False, 4: False}
        step1_fields = ['first_name', 'last_name', 'dob', 'gender', 'email', 'phone']
        step2_fields = ['street', 'city', 'state', 'zip_code', 'country']
        step3_fields = ['high_school', 'graduation_year', 'major', 'enrollment_type']
        step4_fields = ['password', 'confirm_password', 'terms']

        if form.errors:
            for f in step1_fields:
                if f in form.errors:
                    step_errors[1] = True
            for f in step2_fields:
                if f in form.errors:
                    step_errors[2] = True
            for f in step3_fields:
                if f in form.errors:
                    step_errors[3] = True
            for f in step4_fields:
                if f in form.errors:
                    step_errors[4] = True

        return render_template('register.html', form=form, step_errors=step_errors)

    @app.route('/confirmation')
    def confirmation():
        student_id = session.pop('new_student_id', None)
        student_name = session.pop('new_student_name', None)
        if not student_id:
            return redirect(url_for('register'))
        return render_template('confirmation.html', student_id=student_id, student_name=student_name)

    # -----------------------------------------------------------------------
    # Login / Logout
    # -----------------------------------------------------------------------
    @app.route('/login', methods=['GET', 'POST'])
    @limiter.limit("20 per hour")
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        form = LoginForm()
        if form.validate_on_submit():
            student = Student.query.filter_by(email=form.email.data.lower().strip()).first()
            if student and student.check_password(form.password.data):
                login_user(student, remember=form.remember_me.data)
                logger.info(f"Student login: {student.email}")
                audit_logger.log_auth_event(
                    'LOGIN',
                    str(student.id),
                    True,
                    {'email': student.email}
                )
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard'))
            
            audit_logger.log_auth_event(
                'LOGIN',
                form.email.data.lower().strip(),
                False,
                {'reason': 'Invalid credentials'}
            )
            flash('Incorrect email or password. Please try again.', 'error')
            logger.warning(f"Failed login attempt for email: {form.email.data}")

        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logger.info(f"User logout: {current_user.email}")
        audit_logger.log_auth_event('LOGOUT', str(current_user.id), True)
        logout_user()
        flash('You have been signed out.', 'info')
        return redirect(url_for('index'))
    
    # -----------------------------------------------------------------------
    # JWT API endpoints for authentication (v1)
    # -----------------------------------------------------------------------
    @app.route('/api/v1/auth/login', methods=['POST'])
    @limiter.limit("20 per hour")
    def api_login():
        """
        JWT authentication endpoint.
        
        Expected JSON body:
        {
            "email": "user@example.com",
            "password": "SecurePassword123!"
        }
        
        Returns JWT tokens in response.
        """
        try:
            data = request.get_json()
            
            if not data:
                audit_logger.log_auth_event(
                    'LOGIN',
                    'unknown',
                    False,
                    {'reason': 'No JSON body provided'}
                )
                return jsonify({'error': 'Request body is required'}), 400
            
            email = data.get('email', '').strip().lower()
            password = data.get('password', '')
            
            # Validate inputs
            if not email or not password:
                audit_logger.log_auth_event(
                    'LOGIN',
                    email or 'unknown',
                    False,
                    {'reason': 'Missing email or password'}
                )
                return jsonify({'error': 'Email and password are required'}), 400
            
            # Validate email format
            is_valid, error = EmailValidator.validate(email)
            if not is_valid:
                audit_logger.log_auth_event(
                    'LOGIN',
                    email,
                    False,
                    {'reason': 'Invalid email format'}
                )
                return jsonify({'error': error}), 400
            
            # Find student
            student = Student.query.filter_by(email=email).first()
            
            if not student or not student.check_password(password):
                audit_logger.log_auth_event(
                    'LOGIN',
                    email,
                    False,
                    {'reason': 'Invalid credentials'}
                )
                return jsonify({'error': 'Invalid email or password'}), 401
            
            # Generate JWT tokens
            tokens = TokenManager.generate_tokens(
                str(student.id),
                student.email,
                is_admin=False
            )
            
            audit_logger.log_auth_event(
                'LOGIN',
                str(student.id),
                True,
                {'email': student.email}
            )
            
            return jsonify({
                'success': True,
                'user': {
                    'id': student.id,
                    'email': student.email,
                    'first_name': student.first_name,
                },
                'tokens': tokens,
            }), 200
            
        except Exception as e:
            logger.error(f"API login error: {str(e)}")
            audit_logger.log_event(
                'AUTH_ERROR',
                f'Login API error: {str(e)}',
                severity='ERROR'
            )
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/v1/auth/refresh', methods=['POST'])
    @limiter.limit("20 per hour")
    def api_refresh_token():
        """
        Refresh JWT access token using refresh token.
        
        Expected JSON body:
        {
            "refresh_token": "eyJ..."
        }
        """
        try:
            data = request.get_json()
            
            if not data or 'refresh_token' not in data:
                return jsonify({'error': 'Refresh token is required'}), 400
            
            refresh_token = data.get('refresh_token')
            new_tokens = TokenManager.refresh_token(refresh_token)
            
            if not new_tokens:
                return jsonify({'error': 'Invalid or expired refresh token'}), 401
            
            return jsonify({
                'success': True,
                'tokens': new_tokens,
            }), 200
            
        except Exception as e:
            logger.error(f"Token refresh error: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/v1/auth/logout', methods=['POST'])
    @token_required
    def api_logout():
        """Logout via JWT (token becomes invalid after server-side revocation)."""
        audit_logger.log_auth_event(
            'LOGOUT',
            request.user_id,
            True,
            {'method': 'api'}
        )
        return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

    # -----------------------------------------------------------------------
    # Student dashboard & profile
    # -----------------------------------------------------------------------
    @app.route('/dashboard')
    @login_required
    def dashboard():
        if isinstance(current_user, Admin):
            return redirect(url_for('admin_dashboard'))
        return render_template('dashboard.html', student=current_user)

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        if isinstance(current_user, Admin):
            return redirect(url_for('admin_dashboard'))

        form = ProfileUpdateForm(obj=current_user)
        if form.validate_on_submit():
            current_user.first_name = form.first_name.data.strip()
            current_user.last_name = form.last_name.data.strip()
            current_user.phone = form.phone.data.strip()
            current_user.street = form.street.data.strip()
            current_user.city = form.city.data.strip()
            current_user.state = form.state.data.strip()
            current_user.zip_code = form.zip_code.data.strip()
            current_user.country = form.country.data.strip()
            current_user.high_school = form.high_school.data.strip()
            current_user.graduation_year = form.graduation_year.data
            current_user.major = form.major.data
            current_user.enrollment_type = form.enrollment_type.data
            current_user.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))

        return render_template('profile.html', form=form, student=current_user)

    # -----------------------------------------------------------------------
    # Admin routes
    # -----------------------------------------------------------------------
    @app.route('/admin', methods=['GET', 'POST'])
    @limiter.limit("10 per hour")
    def admin_login():
        if current_user.is_authenticated and isinstance(current_user, Admin):
            return redirect(url_for('admin_dashboard'))

        form = AdminLoginForm()
        if form.validate_on_submit():
            admin = Admin.query.filter_by(email=form.email.data.lower().strip()).first()
            if admin and admin.check_password(form.password.data):
                login_user(admin)
                logger.info(f"Admin login: {admin.email}")
                audit_logger.log_auth_event(
                    'LOGIN',
                    str(admin.id),
                    True,
                    {'email': admin.email, 'role': 'admin'}
                )
                return redirect(url_for('admin_dashboard'))
            
            audit_logger.log_auth_event(
                'LOGIN',
                form.email.data.lower().strip(),
                False,
                {'reason': 'Invalid admin credentials', 'role': 'admin'}
            )
            flash('Invalid admin credentials.', 'error')

        return render_template('admin_login.html', form=form)

    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        if not isinstance(current_user, Admin):
            abort(403)
        search = request.args.get('q', '').strip()
        sort = request.args.get('sort', 'registration_date')
        order = request.args.get('order', 'desc')

        query = Student.query
        if search:
            like = f"%{search}%"
            query = query.filter(
                db.or_(
                    Student.first_name.ilike(like),
                    Student.last_name.ilike(like),
                    Student.email.ilike(like),
                    Student.student_id.ilike(like),
                    Student.major.ilike(like),
                )
            )

        col = getattr(Student, sort, Student.registration_date)
        query = query.order_by(col.desc() if order == 'desc' else col.asc())
        students = query.all()

        return render_template(
            'admin_dashboard.html',
            students=students,
            search=search,
            sort=sort,
            order=order,
            total=Student.query.count(),
        )

    # -----------------------------------------------------------------------
    # API – live stats (public, read-only)
    # -----------------------------------------------------------------------
    @app.route('/api/stats')
    def api_stats():
        """Return live enrollment statistics as JSON for charts and counters."""
        from sqlalchemy import func
        total = Student.query.count()
        full_time = Student.query.filter_by(enrollment_type='full_time').count()
        part_time = Student.query.filter_by(enrollment_type='part_time').count()

        major_rows = (
            db.session.query(Student.major, func.count(Student.id).label('cnt'))
            .group_by(Student.major)
            .order_by(func.count(Student.id).desc())
            .all()
        )
        majors = [
            {'name': m.replace('_', ' ').title(), 'count': c}
            for m, c in major_rows
        ]

        # Monthly registrations (last 6 months)
        from datetime import datetime, timedelta
        from sqlalchemy import extract
        monthly = []
        now = datetime.utcnow()
        for i in range(5, -1, -1):
            month_dt = now.replace(day=1) - timedelta(days=i * 30)
            cnt = Student.query.filter(
                extract('year',  Student.registration_date) == month_dt.year,
                extract('month', Student.registration_date) == month_dt.month,
            ).count()
            monthly.append({'month': month_dt.strftime('%b'), 'count': cnt})

        return jsonify({
            'total': total,
            'full_time': full_time,
            'part_time': part_time,
            'majors': majors,
            'monthly': monthly,
        })

    # -----------------------------------------------------------------------
    # Error handlers
    # -----------------------------------------------------------------------
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    # -----------------------------------------------------------------------
    # DB init helper (call once via `flask shell` or the run script)
    # -----------------------------------------------------------------------
    @app.cli.command('init-db')
    def init_db():
        """Create all tables and seed the admin user."""
        db.create_all()
        if not Admin.query.filter_by(email='admin@school.com').first():
            admin = Admin(username='admin', email='admin@school.com')
            admin.set_password('Admin123!')
            db.session.add(admin)
            db.session.commit()
            print('Database initialised and admin user seeded.')
        else:
            print('Database already initialised.')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
