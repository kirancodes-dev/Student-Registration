import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-fallback-secret-change-in-prod'
    WTF_CSRF_ENABLED = True

    # If DATABASE_URL is set, use it directly (supports sqlite:/// or mysql+pymysql://)
    # Otherwise fall back to individual MySQL env vars, or SQLite if no password given.
    _db_url = os.environ.get('DATABASE_URL')
    if not _db_url:
        _db_password = os.environ.get('DB_PASSWORD', '')
        if _db_password:
            _db_host = os.environ.get('DB_HOST', 'localhost')
            _db_port = os.environ.get('DB_PORT', '3306')
            _db_name = os.environ.get('DB_NAME', 'student_registration')
            _db_user = os.environ.get('DB_USER', 'root')
            _db_url = f"mysql+pymysql://{_db_user}:{_db_password}@{_db_host}:{_db_port}/{_db_name}"
        else:
            # SQLite fallback for local development (no MySQL needed)
            _db_url = "sqlite:///student_hub.db"

    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Rate limiting
    RATELIMIT_DEFAULT = "200 per day;50 per hour"
    RATELIMIT_STORAGE_URL = "memory://"
