-- Student Registration System – MySQL Schema
-- Run this ONCE to set up the database, then use `flask init-db` to seed admin.
-- Or run this entire file: mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS student_registration
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE student_registration;

-- ---------------------------------------------------------------
-- Students table
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS students (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    student_id        VARCHAR(20)  NOT NULL UNIQUE,
    first_name        VARCHAR(60)  NOT NULL,
    last_name         VARCHAR(60)  NOT NULL,
    dob               DATE         NOT NULL,
    gender            VARCHAR(20)  NOT NULL,
    email             VARCHAR(120) NOT NULL UNIQUE,
    phone             VARCHAR(20)  NOT NULL,
    street            VARCHAR(200) NOT NULL,
    city              VARCHAR(80)  NOT NULL,
    state             VARCHAR(80)  NOT NULL,
    zip_code          VARCHAR(20)  NOT NULL,
    country           VARCHAR(80)  NOT NULL,
    high_school       VARCHAR(200) NOT NULL,
    graduation_year   INT          NOT NULL,
    major             VARCHAR(100) NOT NULL,
    enrollment_type   VARCHAR(20)  NOT NULL,
    password_hash     VARCHAR(255) NOT NULL,
    registration_date DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_student_id (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------
-- Admins table
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS admins (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(80)  NOT NULL UNIQUE,
    email         VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------
-- Seed admin user  (password: Admin123!)
-- bcrypt hash of 'Admin123!' – regenerated at app start via flask init-db
-- The hash below is illustrative; use `flask init-db` to seed properly.
-- ---------------------------------------------------------------
INSERT IGNORE INTO admins (username, email, password_hash)
VALUES ('admin', 'admin@school.com',
        '$2b$12$PLACEHOLDER_run_flask_init_db_to_get_real_hash');
