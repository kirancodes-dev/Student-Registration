# 🎓 Student Hub – Premium Online Registration System

A production-grade, secure, and feature-rich **Student Online Registration System** built with **Python/Flask**, **SQLAlchemy**, and a premium frontend featuring a tailored design system, full dark mode, and interactive administrative features.

---

## ✨ Features

| Feature Group | Sub-features & Implementation Details |
| :--- | :--- |
| **🎨 Premium UI/UX** | **Apple-HIG inspired interface**: harmony of Deep Navy & Warm Gold, smooth transitions, pill buttons, responsive layouts.<br>**Hero Particle Canvas**: Custom JavaScript floating particles animation.<br>**Bento Feature Grid & Timeline**: Rich visual presentation of system advantages and steps. |
| **🌓 Dark Mode** | Full dark theme support via `data-theme="dark"` styling, local storage preference persistence, and automatic system setting detection. |
| **📋 Multi-step Registration** | 4-step wizard (Personal → Address → Academic → Account) with client-side password strength validation and zero page reloads. Includes auto-dismissing toast notifications. |
| **🚀 Self-Hosted Font Icons** | Bypasses Content Security Policy (CSP) blocking of external CDNs by hosting the **Material Symbols Outlined** font locally under `static/fonts`. |
| **🔐 Security System** | **JWT Authentication** and Flask-Login session separation for students & admins.<br>**Strict Security Headers**: CSP, CORS, X-Frame-Options, X-Content-Type-Options, XSS block, Strict-Transport-Security (HSTS), and Permissions-Policy. |
| **📊 Real-time Stats & Charts** | Dynamic Counter API endpoint (`/api/stats`) feeding live stats to the landing page.<br>**Admin KPI Dashboard**: Student enrollment statistics, majors distribution represented using interactive Chart.js charts, and a real-time searchable/sortable student table. |
| **🛠️ Database Adaptability** | Run in-memory or locally via **SQLite** for development by default, or seamlessly connect to **MySQL 8+** for staging and production environments. |

---

## 🗂️ Project Structure

```
Student-Registration/
├── app.py                  # Main Flask application and route definitions
├── config.py               # Database URI builder (SQLite local fallback vs MySQL prod)
├── models.py               # SQLAlchemy schemas (Student, Admin records)
├── forms.py                # Flask-WTF forms and validation constraints
├── security.py             # Security middleware (CORS configuration, strict CSP/HSTS headers)
├── audit.py                # Audit Logging utility to log secure request/response payloads
├── auth.py                 # JWT token generation, management, and token_required decorators
├── validators.py           # Custom input validators (Email validation, Password strength check)
├── requirements.txt        # Backend python packages list
├── schema.sql              # MySQL raw script for reference/production deployment
├── .env.example            # Environment variables configuration example
├── run.sh                  # Setup, DB initialization, and launch automation script
├── templates/
│   ├── base.html           # Shared layout with local fonts, base styles, dynamic bottom nav & toasts
│   ├── index.html          # Landing page with Canvas particles, stats API, and bento grid
│   ├── register.html       # Interactive multi-step enrollment form
│   ├── login.html          # Secure student sign-in
│   ├── confirmation.html   # Enrollment success page with Confetti overlay and copy ID button
│   ├── dashboard.html      # Student panel with profile completion indicator and courses summary
│   ├── profile.html        # Student profile view and real-time details updates
│   ├── admin_login.html    # Separate secure administrator sign-in page
│   ├── admin_dashboard.html # Admin panel displaying KPI cards, Chart.js graphs, and student table
│   └── 404.html/403.html/500.html # Beautiful custom error page layouts
└── static/
    ├── css/style.css       # Complete custom design system stylesheet (includes local font-face)
    ├── js/main.js          # Client-side form handlers, dark-toggle, stats loading, and animations
    └── fonts/
        └── MaterialSymbolsOutlined.ttf # Self-hosted Google Material Symbols font file
```

---

## ⚙️ Prerequisites

* **Python 3.10+** (Required)
* **MySQL 8+** (Optional – if MySQL is not available, the application automatically falls back to a local SQLite database file `student_hub.db` for easy local development).

---

## 🚀 Quick Start

### Option A: One-Command Start (macOS / Linux)

Run the automated setup and launcher script:
```bash
chmod +x run.sh
./run.sh
```
This script will create a virtual environment (`venv`), install Python requirements, initialize the SQLite database, seed the admin account (`admin@school.com` / `Admin123!`), and start the development server.

### Option B: Manual Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kirancodes-dev/Student-Registration.git
   cd Student-Registration
   ```

2. **Configure environment settings:**
   ```bash
   cp .env.example .env
   # Open .env and adjust variables if connecting to a MySQL server
   ```

3. **Initialize the virtual environment & install packages:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Prepare the database:**
   * **For SQLite (Default)**: Just run the setup command:
     ```bash
     flask --app app init-db
     ```
   * **For MySQL**: Create the schema first:
     ```bash
     mysql -u root -p -e "CREATE DATABASE student_registration CHARACTER SET utf8mb4;"
     flask --app app init-db
     ```

5. **Start the development server:**
   ```bash
   flask --app app run --debug
   ```
   Open **http://127.0.0.1:5000** in your browser.

---

## 🔐 Credentials & Environment (`.env`)

Default Administrator details created during database initialization:
* **URL:** `/admin`
* **Email:** `admin@school.com`
* **Password:** `Admin123!`

```env
SECRET_KEY=your-very-secret-key-change-this-in-production

# MySQL (Leave DB_PASSWORD blank/unset to automatically fall back to SQLite)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=student_registration
DB_USER=root
DB_PASSWORD=your_mysql_password

FLASK_ENV=development
FLASK_DEBUG=1
```

---

## 🛡️ Production & Security Architecture

1. **Self-Hosted Assets**: To satisfy strict network security guidelines, Google Fonts stylesheet is fetched directly from Google Fonts, and the Material Symbols font files are served directly from the application's local `/static/fonts` directory. This stops browsers from blocking icons due to external cross-origin policies.
2. **Robust Content Security Policy (CSP)**:
   ```
   default-src 'self';
   script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;
   style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
   font-src 'self' https://fonts.gstatic.com;
   ```
3. **HTTP Strict Transport Security (HSTS)**: Active on all endpoints, enforcing secure HTTPS connections.
4. **Audit Trail**: Every request and response context is safely logged using custom formatters in `audit.py` to record operations transparently.
5. **Rate Limiting**: Integrated `Flask-Limiter` protecting authentication actions against brute force attacks.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

*Designed with ❤️ in alignment with the Google Material Design & Apple HIG guidelines.*
