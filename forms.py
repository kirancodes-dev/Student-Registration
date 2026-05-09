from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SelectField, BooleanField,
    IntegerField, DateField, TelField, EmailField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length,
    Regexp, NumberRange, ValidationError
)
from models import Student
from datetime import date


MAJORS = [
    ('', 'Select a Major'),
    ('computer_science', 'Computer Science'),
    ('software_engineering', 'Software Engineering'),
    ('data_science', 'Data Science & AI'),
    ('cybersecurity', 'Cybersecurity'),
    ('business_admin', 'Business Administration'),
    ('marketing', 'Marketing'),
    ('finance', 'Finance & Economics'),
    ('biology', 'Biology'),
    ('chemistry', 'Chemistry'),
    ('physics', 'Physics'),
    ('mathematics', 'Mathematics'),
    ('english', 'English Literature'),
    ('psychology', 'Psychology'),
    ('nursing', 'Nursing'),
    ('mechanical_eng', 'Mechanical Engineering'),
    ('electrical_eng', 'Electrical Engineering'),
    ('civil_eng', 'Civil Engineering'),
    ('architecture', 'Architecture'),
    ('graphic_design', 'Graphic Design'),
    ('film_media', 'Film & Media Studies'),
]

GENDERS = [
    ('', 'Select Gender'),
    ('male', 'Male'),
    ('female', 'Female'),
    ('non_binary', 'Non-binary'),
    ('prefer_not', 'Prefer not to say'),
]

ENROLLMENT_TYPES = [
    ('', 'Select Enrollment Type'),
    ('full_time', 'Full-time'),
    ('part_time', 'Part-time'),
]


class RegistrationForm(FlaskForm):
    # Step 1 – Personal
    first_name = StringField('First Name', validators=[
        DataRequired(), Length(min=2, max=60)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(), Length(min=2, max=60)
    ])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=GENDERS, validators=[DataRequired()])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    phone = TelField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^\+?[\d\s\-\(\)]{7,20}$', message='Enter a valid phone number')
    ])

    # Step 2 – Address
    street = StringField('Street Address', validators=[DataRequired(), Length(max=200)])
    city = StringField('City', validators=[DataRequired(), Length(max=80)])
    state = StringField('State / Province', validators=[DataRequired(), Length(max=80)])
    zip_code = StringField('ZIP / Postal Code', validators=[DataRequired(), Length(max=20)])
    country = StringField('Country', validators=[DataRequired(), Length(max=80)])

    # Step 3 – Academic
    high_school = StringField('High School Name', validators=[DataRequired(), Length(max=200)])
    graduation_year = IntegerField('Graduation Year', validators=[
        DataRequired(), NumberRange(min=1990, max=date.today().year + 4)
    ])
    major = SelectField('Desired Major / Program', choices=MAJORS, validators=[DataRequired()])
    enrollment_type = SelectField('Enrollment Type', choices=ENROLLMENT_TYPES, validators=[DataRequired()])

    # Step 4 – Account
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters'),
        Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
            message='Must include uppercase, lowercase, and a number'
        )
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    terms = BooleanField('I agree to the Terms & Conditions', validators=[DataRequired()])

    def validate_email(self, field):
        if Student.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('An account with this email already exists.')

    def validate_dob(self, field):
        if field.data and field.data >= date.today():
            raise ValidationError('Date of birth must be in the past.')


class LoginForm(FlaskForm):
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me signed in')


class AdminLoginForm(FlaskForm):
    email = EmailField('Admin Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class ProfileUpdateForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=60)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=60)])
    phone = TelField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^\+?[\d\s\-\(\)]{7,20}$', message='Enter a valid phone number')
    ])
    street = StringField('Street Address', validators=[DataRequired(), Length(max=200)])
    city = StringField('City', validators=[DataRequired(), Length(max=80)])
    state = StringField('State / Province', validators=[DataRequired(), Length(max=80)])
    zip_code = StringField('ZIP / Postal Code', validators=[DataRequired(), Length(max=20)])
    country = StringField('Country', validators=[DataRequired(), Length(max=80)])
    high_school = StringField('High School Name', validators=[DataRequired(), Length(max=200)])
    graduation_year = IntegerField('Graduation Year', validators=[
        DataRequired(), NumberRange(min=1990, max=date.today().year + 4)
    ])
    major = SelectField('Major / Program', choices=MAJORS, validators=[DataRequired()])
    enrollment_type = SelectField('Enrollment Type', choices=ENROLLMENT_TYPES, validators=[DataRequired()])
