import random
import string
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def generate_student_id():
    """Generate a unique student ID like STU-2025-XXXX."""
    year = datetime.now().year
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"STU-{year}-{suffix}"


class Student(UserMixin, db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)

    # Personal
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    # Address
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(80), nullable=False)

    # Academic
    high_school = db.Column(db.String(200), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    major = db.Column(db.String(100), nullable=False)
    enrollment_type = db.Column(db.String(20), nullable=False)  # full-time / part-time

    # Account
    password_hash = db.Column(db.String(255), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def profile_completion(self):
        """Return profile completion percentage."""
        fields = [
            self.first_name, self.last_name, self.dob, self.gender,
            self.email, self.phone, self.street, self.city, self.state,
            self.zip_code, self.country, self.high_school,
            self.graduation_year, self.major, self.enrollment_type,
        ]
        filled = sum(1 for f in fields if f)
        return int((filled / len(fields)) * 100)


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Distinguish admin sessions from student sessions
    is_admin = True

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_id(self):
        return f"admin-{self.id}"
