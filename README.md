# 🎓 Student Hub – Online Registration System

A production-ready **Student Online Registration System** built with **Python / Flask**, **MySQL**, and a clean **Apple HIG-inspired UI**. Multi-step form, student dashboard, profile management, and an admin panel – all wrapped in a polished, mobile-first design.

---

## ✨ Features

| Feature | Details |
|---|---|
| **Multi-step Registration** | 4-step form (Personal → Address → Academic → Account) with live validation, progress indicator, and zero page reloads |
| **Unique Student ID** | Auto-generated IDs like `STU-2026-A3F9` on successful registration |
| **Student Dashboard** | Profile completion ring, upcoming deadlines, quick-action cards |
| **Profile Management** | View & update all details; read-only Student ID and registration date |
| **Admin Panel** | Searchable, sortable student table at `/admin` |
| **Security** | bcrypt passwords, CSRF protection (Flask-WTF), rate limiting on auth routes, input sanitisation |
| **Apple-like UI** | System fonts, backdrop blur nav, pill buttons, iOS toggle switches, subtle micro-animations |
| **Responsive** | Mobile-first CSS, works on phone, tablet, and desktop |
| **Custom Error Pages** | Styled 404, 403, and 500 pages |

---

## 🗂️ Project Structure

```
Student-Registration/
├── app.py               # Flask app factory + all routes
├── config.py            # Config from environment variables
├── models.py            # SQLAlchemy models (Student, Admin)
├── forms.py             # Flask-WTF forms with validators
├── requirements.txt     # Python dependencies
├── schema.sql           # MySQL schema (reference / manual setup)
├── .env.example         # Environment variable template
├── run.sh               # One-command setup & run script
├── templates/
│   ├── base.html        # Shared layout with nav & flash messages
│   ├── index.html       # Landing page
│   ├── register.html    # Multi-step registration form
│   ├── login.html       # Student login
│   ├── confirmation.html# Post-registration success page
│   ├── dashboard.html   # Student dashboard
│   ├── profile.html     # Profile view & edit
│   ├── admin_login.html # Admin login
│   ├── admin_dashboard.html  # Admin student table
│   ├── 404.html / 403.html / 500.html
└── static/
    ├── css/style.css    # Full Apple-like stylesheet (~600 lines)
    └── js/main.js       # Multi-step logic, password meter, animations
```

---

## ⚙️ Prerequisites

> **Do you need to install MySQL?** → **Yes.** This app requires a running MySQL server. See the section below.

### 1. MySQL

#### macOS (Homebrew)
```bash
brew install mysql
brew services start mysql
mysql_secure_installation    # set a root password
```

#### Ubuntu / Debian
```bash
sudo apt update && sudo apt install mysql-server -y
sudo systemctl start mysql
sudo mysql_secure_installation
```

#### Windows
Download and run the [MySQL Installer](https://dev.mysql.com/downloads/installer/) (choose MySQL Server + MySQL Workbench).

---

### 2. Python 3.10+

```bash
python3 --version   # should be 3.10 or higher
```

Download from [python.org](https://www.python.org/downloads/) if needed.

---

## 🚀 Quick Start

### Option A – One command (macOS / Linux)

```bash
git clone https://github.com/kirancodes-dev/Student-Registration.git
cd Student-Registration
chmod +x run.sh
./run.sh
```

This script will:
1. Copy `.env.example` → `.env` (edit it with your MySQL credentials)
2. Create a Python virtual environment
3. Install all dependencies
4. Create database tables and seed the admin user
5. Start the Flask dev server on **http://localhost:5000**

---

### Option B – Manual Setup

```bash
# 1. Clone
git clone https://github.com/kirancodes-dev/Student-Registration.git
cd Student-Registration

# 2. Configure environment
cp .env.example .env
# Open .env and fill in your MySQL credentials

# 3. Create the MySQL database
mysql -u root -p -e "CREATE DATABASE student_registration CHARACTER SET utf8mb4;"

# 4. Python virtual environment
python3 -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Create tables + seed admin
flask --app app init-db

# 7. Run
flask --app app run --debug
```

Open **http://localhost:5000**

---

## 🔐 Environment Variables (`.env`)

```env
SECRET_KEY=your-very-secret-key-change-this-in-production

DB_HOST=localhost
DB_PORT=3306
DB_NAME=student_registration
DB_USER=root
DB_PASSWORD=your_mysql_password

FLASK_ENV=development
FLASK_DEBUG=1
```

---

## 🛡️ Admin Panel

| URL | `/admin` |
|---|---|
| Email | `admin@school.com` |
| Password | `Admin123!` |

The admin panel shows a searchable, sortable table of all registered students.

---

## 🗄️ Database Schema

| Table | Key Columns |
|---|---|
| `students` | `student_id` (unique), personal info, address, academic, `password_hash`, `registration_date` |
| `admins` | `username`, `email`, `password_hash` |

`schema.sql` contains the raw `CREATE TABLE` statements for reference. The `flask init-db` command handles creation automatically via SQLAlchemy.

---

## 🔒 Security Highlights

- Passwords hashed with **bcrypt** (cost factor 12)
- **CSRF tokens** on every form via Flask-WTF
- **Rate limiting**: 10 registrations/hour, 20 logins/hour per IP
- Email uniqueness enforced at both DB and form-validation levels
- Input stripped and sanitised before persistence
- Admin and student sessions are separate user types

---

## 🌐 Production Deployment (optional)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:app"
```

Put Nginx in front as a reverse proxy and set `FLASK_ENV=production` in your `.env`.

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask 3, Flask-Login, Flask-WTF, Flask-Bcrypt |
| ORM | SQLAlchemy 2, PyMySQL |
| Database | MySQL 8+ |
| Frontend | HTML5, CSS3 (custom Apple HIG design), Vanilla JS |
| Security | Flask-Limiter, bcrypt, CSRF |

---

## 📄 License

MIT – see [LICENSE](LICENSE)

---

*Built with Flask & ♥ — inspired by Apple's Human Interface Guidelines.*
