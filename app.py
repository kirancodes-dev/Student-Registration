import logging
from datetime import datetime
from flask import (
    Flask, render_template, redirect, url_for,
    flash, request, session, abort
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

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

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

    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    logger = logging.getLogger(__name__)

    # -----------------------------------------------------------------------
    # User loader – handles both Student and Admin sessions
    # -----------------------------------------------------------------------
    @login_manager.user_loader
    def load_user(user_id):
        if str(user_id).startswith('admin-'):
            admin_id = int(user_id.split('-')[1])
            return Admin.query.get(admin_id)
        return Student.query.get(int(user_id))

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
            session['new_student_id'] = student.student_id
            session['new_student_name'] = student.first_name
            return redirect(url_for('confirmation'))

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
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard'))
            flash('Incorrect email or password. Please try again.', 'error')
            logger.warning(f"Failed login attempt for email: {form.email.data}")

        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logger.info(f"User logout: {current_user.email}")
        logout_user()
        flash('You have been signed out.', 'info')
        return redirect(url_for('index'))

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
                return redirect(url_for('admin_dashboard'))
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
