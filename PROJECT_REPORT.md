# Student Hub — Online Registration System
## Final Project Report

**Author:** Kiran Biradar  
**Date:** May 2026  
**GitHub:** https://github.com/kirancodes-dev/Student-Registration  
**Live URL:** http://127.0.0.1:5001

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [System Architecture](#3-system-architecture)
4. [Database Schema](#4-database-schema)
5. [Key Logic & Code Walkthrough](#5-key-logic--code-walkthrough)
6. [Registered Students (All 20)](#6-registered-students-all-20)
7. [Course Catalog (All 12 Courses)](#7-course-catalog-all-12-courses)
8. [Application Pages & Features](#8-application-pages--features)
9. [Security Features](#9-security-features)
10. [Step-by-Step Setup Guide](#10-step-by-step-setup-guide)

---

## 1. Project Overview

**Student Hub** is a full-stack, production-quality Student Online Registration System built with Python (Flask) on the backend and a Material Design 3 interface on the frontend. The system allows students to register, log in, manage their profile, discover courses, and view their academic dashboard. An admin panel provides a searchable, sortable view of all enrolled students.

### Goals
- Replace paper-based enrollment with a digital, secure web system
- Provide students a personalised dashboard with profile completion tracking
- Give administrators a real-time view of all registrations
- Demonstrate a complete MVC web application with industry-standard security

---

## 2. Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend | Python 3.12, Flask 3.0 | Web framework, routing, templating |
| ORM | SQLAlchemy 3.1 | Database models and queries |
| Database | MySQL 8.0 (dev) / SQLite (fallback) | Persistent student data storage |
| Auth | Flask-Login, Flask-Bcrypt | Session management, password hashing |
| Forms | Flask-WTF, WTForms | CSRF-protected form validation |
| Rate Limiting | Flask-Limiter | Brute-force protection on auth routes |
| Frontend | Tailwind CSS (CDN), Material Design 3 | UI design system |
| Icons | Material Symbols Outlined | Consistent icon set |
| Font | Public Sans (Google Fonts) | Clean, readable typeface |
| JS | Vanilla JavaScript (main.js) | Multi-step form, password strength |
| Config | python-dotenv | Environment variable management |
| MySQL Driver | PyMySQL | Python-to-MySQL connection |

---

## 3. System Architecture

```
Student-Registration/
├── app.py              ← Flask app factory + all routes (315 lines)
├── models.py           ← SQLAlchemy ORM: Student, Admin models
├── forms.py            ← Flask-WTF forms with validation
├── config.py           ← Environment-based configuration
├── seed_students.py    ← Sample data loader (20 students)
├── .env                ← Secrets (not committed to git)
├── requirements.txt    ← Python dependencies
├── templates/
│   ├── base.html       ← Master layout: top app bar, bottom nav, flash
│   ├── index.html      ← Public landing page
│   ├── register.html   ← 4-step registration form
│   ├── login.html      ← Student login
│   ├── dashboard.html  ← Student home with progress card
│   ├── profile.html    ← Edit personal/academic details
│   ├── courses.html    ← Searchable course catalog
│   ├── admin_login.html
│   ├── admin_dashboard.html ← Searchable student table
│   └── confirmation.html
└── static/
    ├── js/main.js      ← Multi-step form + password strength JS
    └── css/, img/
```

### Request Flow

```
Browser → Flask Route → Form Validation → SQLAlchemy ORM → MySQL
                                                          ↓
Browser ← Jinja2 Template ← Python Logic ← Query Result ←┘
```

---

## 4. Database Schema

### `students` table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | Internal row ID |
| student_id | VARCHAR(20) | UNIQUE, NOT NULL | e.g. STU-2026-KWLF |
| first_name | VARCHAR(60) | NOT NULL | |
| last_name | VARCHAR(60) | NOT NULL | |
| dob | DATE | NOT NULL | Date of birth |
| gender | VARCHAR(20) | NOT NULL | male / female / non_binary |
| email | VARCHAR(120) | UNIQUE, NOT NULL | Login credential |
| phone | VARCHAR(20) | NOT NULL | |
| street | VARCHAR(200) | NOT NULL | |
| city | VARCHAR(80) | NOT NULL | |
| state | VARCHAR(80) | NOT NULL | |
| zip_code | VARCHAR(20) | NOT NULL | |
| country | VARCHAR(80) | NOT NULL | |
| high_school | VARCHAR(200) | NOT NULL | Previous institution |
| graduation_year | INTEGER | NOT NULL | Year HS was completed |
| major | VARCHAR(100) | NOT NULL | Chosen program |
| enrollment_type | VARCHAR(20) | NOT NULL | full_time / part_time |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt hash |
| registration_date | DATETIME | DEFAULT NOW | Auto-set on insert |
| updated_at | DATETIME | DEFAULT NOW | Auto-update on edit |

### `admins` table

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK |
| username | VARCHAR(80) | UNIQUE |
| email | VARCHAR(120) | UNIQUE |
| password_hash | VARCHAR(255) | NOT NULL |

---

## 5. Key Logic & Code Walkthrough

### 5.1 App Factory Pattern — `app.py`

The application uses Flask's **app factory pattern**, which creates the app inside a function. This enables clean testing and multiple configurations.

```python
# app.py — Lines 22–48
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)   # load from config.py

    db.init_app(app)                 # SQLAlchemy binds to app
    bcrypt.init_app(app)             # Bcrypt for password hashing

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'  # redirect unauthenticated users here

    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
    )
    ...
    return app
```

**Why app factory?** — Allows `create_app()` to be called with test configs. All extensions are initialized against the app instance, not at module level. This avoids circular import issues.

---

### 5.2 Unique Student ID Generator — `models.py`

```python
# models.py — Lines 12–16
def generate_student_id():
    """Generate a unique student ID like STU-2026-XXXX."""
    year = datetime.now().year
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"STU-{year}-{suffix}"
```

Called during registration with a **collision-retry loop**:

```python
# app.py — Lines 93–95
sid = generate_student_id()
while Student.query.filter_by(student_id=sid).first():
    sid = generate_student_id()   # retry on collision
```

**Key insight:** The 4-character suffix using 36 characters (A-Z + 0-9) gives 36^4 = 1,679,616 possible IDs per year. The while-loop ensures uniqueness even in edge-case collisions.

---

### 5.3 Password Hashing — `models.py`

```python
# models.py — Lines 51–55
def set_password(self, password):
    self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(self, password):
    return bcrypt.check_password_hash(self.password_hash, password)
```

**Why bcrypt?** — bcrypt is a one-way adaptive hash. Even if the database is compromised, raw passwords cannot be recovered. The work factor automatically slows brute-force attacks.

**Registration validation** in `forms.py`:
```python
# forms.py — Lines 86–91
password = PasswordField('Password', validators=[
    DataRequired(),
    Length(min=8),
    Regexp(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
        message='Must include uppercase, lowercase, and a number'
    )
])
```

---

### 5.4 Dual-Role Login (Student + Admin) — `app.py`

```python
# app.py — Lines 52–57
@login_manager.user_loader
def load_user(user_id):
    if str(user_id).startswith('admin-'):
        admin_id = int(user_id.split('-')[1])
        return Admin.query.get(admin_id)
    return Student.query.get(int(user_id))
```

Admin IDs are stored in the session as `admin-1`, `admin-2` etc., while students use plain integers. This lets a single `login_manager` handle both user types.

The `Admin.get_id()` method makes this work:
```python
# models.py — Lines 91–92
def get_id(self):
    return f"admin-{self.id}"   # prefix distinguishes from student IDs
```

---

### 5.5 Profile Completion Property — `models.py`

```python
# models.py — Lines 57–71
@property
def profile_completion(self):
    fields = [
        self.first_name, self.last_name, self.dob, self.gender,
        self.email, self.phone, self.street, self.city, self.state,
        self.zip_code, self.country, self.high_school,
        self.graduation_year, self.major, self.enrollment_type,
    ]
    filled = sum(1 for f in fields if f)
    return int((filled / len(fields)) * 100)
```

Returns a percentage (0–100) used to render the animated progress bar on the dashboard. Students see how complete their registration is and are nudged to fill in missing fields.

---

### 5.6 Admin Search & Sort — `app.py`

```python
# app.py — Lines 248–266
search = request.args.get('q', '').strip()
sort   = request.args.get('sort', 'registration_date')
order  = request.args.get('order', 'desc')

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
```

**Key patterns:**
- `ilike()` = case-insensitive LIKE query (works in both MySQL and SQLite)
- `db.or_()` = SQLAlchemy's OR combinator — searches across 5 columns simultaneously
- `getattr(Student, sort, ...)` = dynamic column selection from URL param, with safe fallback

---

### 5.7 Database URL Encoding Fix — `config.py`

```python
# config.py — Lines 2, 21
from urllib.parse import quote_plus

_db_url = f"mysql+pymysql://{_db_user}:{quote_plus(_db_password)}@{_db_host}:{_db_port}/{_db_name}"
```

**Problem:** Passwords with special characters like `@`, `#`, `/` break the database URL because those characters are URL delimiters. For example, `Kiran123@` would cause the parser to treat `localhost` as the password and fail to find the host.

**Solution:** `quote_plus()` encodes `@` → `%40`, `#` → `%23`, making the URL safe.

---

### 5.8 Multi-Step Form Controller — `static/js/main.js`

```javascript
// main.js — Lines 14–106
(function initMultiStep() {
  const panels = document.querySelectorAll('.form-panel');
  let current  = 0;

  // Auto-jump to first panel that has server-side errors
  document.querySelectorAll('.field-error').forEach(el => {
    const panel = el.closest('.form-panel');
    if (panel) {
      const idx = [...panels].indexOf(panel);
      if (idx < current || current === 0) current = idx;
    }
  });

  function showStep(idx) {
    panels.forEach((p, i) => p.classList.toggle('hidden', i !== idx));
    // update step dots, progress bar, title label...
    current = idx;
  }

  // Client-side validation before moving to next step
  function validateStep(idx) {
    let ok = true;
    (stepFields[idx] || []).forEach(name => {
      const el = form.querySelector(`[name="${name}"]`);
      if (el.required && !el.value.trim()) ok = false;
    });
    return ok;
  }
})();
```

**Key behaviours:**
1. Shows only the active `.form-panel`, hides others with Tailwind's `hidden` class
2. If Flask returns validation errors, JS reads `.field-error` elements and automatically jumps to the first step with errors
3. "Next" buttons validate the current step client-side before advancing
4. Final submit validates all 4 steps and blocks if any fail

---

### 5.9 SQLite Fallback — `config.py`

```python
# config.py — Lines 13–24
_db_url = os.environ.get('DATABASE_URL')
if not _db_url:
    _db_password = os.environ.get('DB_PASSWORD', '')
    if _db_password:
        _db_url = f"mysql+pymysql://..."
    else:
        _db_url = "sqlite:///student_hub.db"   # fallback
```

If `DB_PASSWORD` is not set in `.env`, the app automatically uses SQLite — no MySQL installation needed. This makes onboarding simple for new developers.

---

## 6. Registered Students (All 20)

| # | Student ID | Name | Email | Major | Type | City |
|---|-----------|------|-------|-------|------|------|
| 1 | STU-2026-KWLF | Emma Johnson | emma.johnson@email.com | Computer Science | Full-time | San Francisco, CA |
| 2 | STU-2026-8R5X | Liam Williams | liam.williams@email.com | Data Science | Full-time | Los Angeles, CA |
| 3 | STU-2026-GD4L | Sophia Brown | sophia.brown@email.com | Psychology | Part-time | Chicago, IL |
| 4 | STU-2026-DM6R | Noah Davis | noah.davis@email.com | Software Engineering | Full-time | Austin, TX |
| 5 | STU-2026-QSI5 | Olivia Martinez | olivia.martinez@email.com | Business Admin | Full-time | Miami, FL |
| 6 | STU-2026-WUCK | Ethan Garcia | ethan.garcia@email.com | Cybersecurity | Part-time | Phoenix, AZ |
| 7 | STU-2026-B8JW | Ava Wilson | ava.wilson@email.com | Graphic Design | Full-time | Seattle, WA |
| 8 | STU-2026-7Q8J | James Anderson | james.anderson@email.com | Mathematics | Full-time | Boston, MA |
| 9 | STU-2026-GH8K | Isabella Taylor | isabella.taylor@email.com | Nursing | Full-time | Atlanta, GA |
| 10 | STU-2026-VTM0 | Lucas Thomas | lucas.thomas@email.com | Mechanical Eng | Part-time | Denver, CO |
| 11 | STU-2026-3MJ8 | Mia Jackson | mia.jackson@email.com | Electrical Eng | Full-time | Portland, OR |
| 12 | STU-2026-Z241 | Benjamin White | benjamin.white@email.com | Finance | Full-time | Las Vegas, NV |
| 13 | STU-2026-BGBQ | Charlotte Harris | charlotte.harris@email.com | Marketing | Part-time | Nashville, TN |
| 14 | STU-2026-75FL | Alexander Lee | alexander.lee@email.com | Civil Eng | Full-time | Honolulu, HI |
| 15 | STU-2026-BIEQ | Amelia Clark | amelia.clark@email.com | Biology | Full-time | Anchorage, AK |
| 16 | STU-2026-EZWH | Henry Lewis | henry.lewis@email.com | Architecture | Part-time | Albuquerque, NM |
| 17 | STU-2026-L4WH | Evelyn Robinson | evelyn.robinson@email.com | Chemistry | Full-time | Raleigh, NC |
| 18 | STU-2026-URRE | Sebastian Walker | sebastian.walker@email.com | Film & Media | Part-time | Indianapolis, IN |
| 19 | STU-2026-05T0 | Harper Hall | harper.hall@email.com | English Literature | Full-time | Louisville, KY |
| 20 | STU-2026-3M3W | Daniel Young | daniel.young@email.com | Physics | Full-time | Providence, RI |

**Enrollment breakdown:** 14 full-time (70%) · 6 part-time (30%)  
**Gender breakdown:** 10 female · 10 male  
**States represented:** CA, IL, TX, FL, AZ, WA, MA, GA, CO, OR, NV, TN, HI, AK, NM, NC, IN, KY, RI

---

## 7. Course Catalog (All 12 Courses)

| Code | Course Name | Credits | Professor | Enrolled | Dept | Tag |
|------|------------|---------|-----------|----------|------|-----|
| CS101 | Introduction to Programming | 4 | Dr. Sarah Chen | 120 | Computer Science | Foundation |
| CS302 | Advanced Algorithms | 4 | Dr. Sarah Chen | 26 | Computer Science | Core |
| CS402 | Advanced Software Architecture | 4 | Prof. James Ko | 18 | Computer Science | Core |
| DS201 | Machine Learning Fundamentals | 3 | Dr. Priya Nair | 55 | Data Science | Core |
| DS310 | Deep Learning & Neural Networks | 3 | Dr. Priya Nair | 31 | Data Science | Advanced |
| CYB201 | Network Security & Cryptography | 4 | Prof. Marcus Reid | 40 | Cybersecurity | Core |
| MAT215 | Complex Variables & Analysis | 3 | Dr. James Wilson | 0 | Mathematics | Elective |
| MAT310 | Linear Algebra & Applications | 3 | Dr. James Wilson | 62 | Mathematics | Core |
| PHY101 | Introduction to Physics I | 4 | Prof. Linda Hayes | 104 | Sciences | Lab Required |
| BUS301 | Data-Driven Decision Making | 3 | Prof. R. Torres | 42 | Business | Cross-listed |
| NUR201 | Clinical Nursing Practice I | 4 | Prof. Angela Moore | 38 | Nursing | Lab Required |
| HU210 | Digital Ethics & Society | 3 | Dr. Aisha Patel | 34 | Humanities | Elective |

**Total credits offered:** 41 credits  
**Average class size:** 47.5 students  
**Largest class:** CS101 — 120 students  
**Lab courses:** PHY101, NUR201

---

## 8. Application Pages & Features

### Public Pages
| URL | Page | Description |
|-----|------|-------------|
| `/` | Landing Page | Hero section, feature grid, stats strip |
| `/register` | 4-Step Registration | Personal → Address → Academic → Account |
| `/login` | Student Login | Email + password with rate limiting |
| `/admin` | Admin Login | Separate admin login portal |

### Authenticated Student Pages
| URL | Page | Description |
|-----|------|-------------|
| `/dashboard` | Student Dashboard | Progress card, quick links, deadlines |
| `/profile` | Edit Profile | Update all personal and academic details |
| `/courses` | Course Discovery | Searchable catalog of 12 courses |
| `/logout` | Logout | Clears session, redirects to home |

### Admin Pages
| URL | Page | Description |
|-----|------|-------------|
| `/admin/dashboard` | Admin Panel | All students, search, sort by any column |

---

## 9. Security Features

| Feature | Implementation | Purpose |
|---------|---------------|---------|
| Password hashing | Flask-Bcrypt with cost factor | Protects passwords if DB is compromised |
| CSRF protection | Flask-WTF (all forms) | Prevents cross-site request forgery |
| Rate limiting | Flask-Limiter (10/hr register, 20/hr login) | Stops brute-force and bot attacks |
| Session management | Flask-Login with secure cookies | Proper auth state management |
| Input validation | WTForms validators + custom checks | Rejects malformed or duplicate data |
| URL encoding | urllib.parse.quote_plus | Handles special chars in DB credentials |
| Admin isolation | `isinstance(current_user, Admin)` guards | Students cannot access admin routes |
| 403 / 404 handlers | Custom error pages | Prevents information leakage |
| .env file | python-dotenv, not committed to git | Secrets never in version control |

---

## 10. Step-by-Step Setup Guide

This final section explains exactly how to go from a blank Mac to a running Student Hub application.

---

### Step 1 — Install Homebrew

Homebrew is the Mac package manager. Open Terminal and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After it finishes, add Homebrew to your PATH (Apple Silicon Mac):
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Verify:
```bash
brew --version   # should print: Homebrew 4.x.x
```

---

### Step 2 — Install MySQL

```bash
brew install mysql
brew services start mysql        # start MySQL automatically on boot
/opt/homebrew/bin/mysql_secure_installation
```

When prompted:
- Press **Enter** for current password (no password yet)
- Type `1` for MEDIUM password policy
- Enter a strong password (e.g. `Kiran123@`) — **remember this**
- Answer `Y` to all remaining questions

---

### Step 3 — Create the Database

```bash
/opt/homebrew/bin/mysql -u root -p
```

Enter your MySQL password, then:
```sql
CREATE DATABASE student_registration;
EXIT;
```

---

### Step 4 — Clone the Repository

```bash
cd ~
mkdir Student && cd Student
git clone https://github.com/kirancodes-dev/Student-Registration.git
cd Student-Registration
```

---

### Step 5 — Create Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Step 6 — Configure Environment Variables

Create a `.env` file in the project root:
```bash
nano .env
```

Paste:
```env
SECRET_KEY=student-hub-secret-key-change-in-prod
DB_HOST=localhost
DB_PORT=3306
DB_NAME=student_registration
DB_USER=root
DB_PASSWORD=YourMySQLPasswordHere
FLASK_ENV=development
FLASK_DEBUG=1
```

Save: `Ctrl+X`, then `Y`, then `Enter`.

---

### Step 7 — Initialise the Database

This creates all tables and seeds the admin account:
```bash
flask --app app init-db
```

Expected output:
```
Database initialised and admin user seeded.
```

---

### Step 8 — Load Sample Student Data

```bash
python seed_students.py
```

Expected output:
```
  ADD   STU-2026-XXXX  Emma Johnson — computer_science
  ...
✅  Done! 20 students added, 0 skipped.
    Total students in DB: 20
```

---

### Step 9 — Start the Application

```bash
flask --app app run --debug --port 5001
```

> **Note:** Port 5000 is used by macOS AirPlay. Always use port 5001.

Expected output:
```
 * Running on http://127.0.0.1:5001
 * Debug mode: on
```

---

### Step 10 — Open in Browser

| URL | Purpose | Login |
|-----|---------|-------|
| http://127.0.0.1:5001 | Landing page | No login needed |
| http://127.0.0.1:5001/register | Register a new student | No login needed |
| http://127.0.0.1:5001/login | Student login | Any seeded email + password |
| http://127.0.0.1:5001/admin | Admin panel | admin@school.com / Admin123! |

**Sample student login:**
```
Email:    emma.johnson@email.com
Password: Emma@1234
```

---

### Verify Database Directly (Optional)

```bash
/opt/homebrew/bin/mysql -u root -p student_registration
```

```sql
-- View all students
SELECT student_id, first_name, last_name, major FROM students;

-- Count enrollments
SELECT COUNT(*) FROM students;

-- View admin accounts
SELECT username, email FROM admins;

-- Show all tables
SHOW TABLES;
```

---

## Summary

| Metric | Value |
|--------|-------|
| Total students registered | 20 |
| Total courses available | 12 |
| Lines of Python code | ~450 |
| Lines of HTML/Jinja2 | ~900 |
| Lines of JavaScript | ~130 |
| Database tables | 2 (students, admins) |
| Security layers | 7 (bcrypt, CSRF, rate limit, login, validation, encoding, isolation) |
| GitHub commits | 4 |

---

*Student Hub — Built with Flask, SQLAlchemy, MySQL, and Material Design 3*  
*GitHub: https://github.com/kirancodes-dev/Student-Registration*
