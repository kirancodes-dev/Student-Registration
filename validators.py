"""
Input validation utilities for the Student Registration System.
Provides email validation, password strength checking, and XSS/SQL injection prevention.
"""

import re
from typing import Tuple, Optional
from html import escape


class EmailValidator:
    """Validates email addresses according to RFC 5322."""
    
    # Simplified but comprehensive email regex
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    )
    
    @staticmethod
    def validate(email: str) -> Tuple[bool, Optional[str]]:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email or not isinstance(email, str):
            return False, "Email is required"
        
        email = email.strip().lower()
        
        if len(email) > 254:
            return False, "Email is too long (max 254 characters)"
        
        if not EmailValidator.EMAIL_PATTERN.match(email):
            return False, "Invalid email format"
        
        # Check for common disposable email domains (optional)
        disposable_domains = {
            'tempmail.com', 'mailinator.com', '10minutemail.com',
            'throwaway.email', 'fake-mail.com',
        }
        
        domain = email.split('@')[1]
        if domain in disposable_domains:
            return False, "Disposable email addresses are not allowed"
        
        return True, None


class PasswordValidator:
    """Validates password strength and requirements."""
    
    @staticmethod
    def validate(password: str) -> Tuple[bool, Optional[str]]:
        """
        Validate password meets security requirements.
        
        Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not password or not isinstance(password, str):
            return False, "Password is required"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if len(password) > 128:
            return False, "Password is too long (max 128 characters)"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one digit"
        
        special_chars = r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]'
        if not re.search(special_chars, password):
            return False, "Password must contain at least one special character"
        
        # Check for common weak passwords
        weak_passwords = {
            'password', '123456', 'admin', 'letmein', 'welcome',
            'monkey', 'dragon', 'master', 'sunshine', 'princess',
        }
        
        if password.lower() in weak_passwords:
            return False, "Password is too common. Choose a more unique password"
        
        return True, None


class InputSanitizer:
    """Sanitizes user input to prevent XSS and injection attacks."""
    
    # SQL keyword pattern for basic SQL injection detection
    SQL_KEYWORDS = re.compile(
        r'\b(UNION|SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|SCRIPT)\b',
        re.IGNORECASE
    )
    
    # XSS pattern detection
    XSS_PATTERNS = [
        re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL),
        re.compile(r'javascript:', re.IGNORECASE),
        re.compile(r'on\w+\s*=', re.IGNORECASE),  # onclick, onload, etc.
        re.compile(r'<iframe', re.IGNORECASE),
        re.compile(r'<object', re.IGNORECASE),
        re.compile(r'<embed', re.IGNORECASE),
    ]
    
    @staticmethod
    def sanitize_text(text: str, allow_html: bool = False) -> str:
        """
        Sanitize text input to prevent XSS attacks.
        
        Args:
            text: Input text to sanitize
            allow_html: If False, escapes HTML entities
            
        Returns:
            Sanitized text
        """
        if not isinstance(text, str):
            return ""
        
        text = text.strip()
        
        # Remove control characters
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
        
        # Check for XSS patterns
        for pattern in InputSanitizer.XSS_PATTERNS:
            if pattern.search(text):
                text = pattern.sub('', text)
        
        # Escape HTML if not allowed
        if not allow_html:
            text = escape(text)
        
        return text
    
    @staticmethod
    def detect_sql_injection(text: str) -> bool:
        """
        Basic SQL injection detection.
        
        Args:
            text: Input to check
            
        Returns:
            True if potential SQL injection detected
        """
        if not isinstance(text, str):
            return False
        
        # Check for SQL keywords
        if InputSanitizer.SQL_KEYWORDS.search(text):
            return True
        
        # Check for common SQL injection patterns
        sql_patterns = [
            r"('\s*OR\s*')",
            r'("\s*OR\s*")',
            r'(--)', r'(;)',
            r'(/\*.*?\*/)',
            r'(xp_|sp_)',
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    @staticmethod
    def validate_and_sanitize(text: str, field_name: str = "input") -> Tuple[Optional[str], Optional[str]]:
        """
        Validate and sanitize input in one call.
        
        Args:
            text: Input text
            field_name: Name of field for error messages
            
        Returns:
            Tuple of (sanitized_text, error_message)
        """
        if not text or not isinstance(text, str):
            return None, f"{field_name} is required"
        
        if InputSanitizer.detect_sql_injection(text):
            return None, f"{field_name} contains invalid characters"
        
        sanitized = InputSanitizer.sanitize_text(text)
        
        if not sanitized:
            return None, f"{field_name} is empty after sanitization"
        
        return sanitized, None


class NameValidator:
    """Validates names for registration forms."""
    
    @staticmethod
    def validate(name: str, field_name: str = "Name") -> Tuple[bool, Optional[str]]:
        """
        Validate name format.
        
        Args:
            name: Name to validate
            field_name: Name of field for error messages
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name or not isinstance(name, str):
            return False, f"{field_name} is required"
        
        name = name.strip()
        
        if len(name) < 2:
            return False, f"{field_name} must be at least 2 characters long"
        
        if len(name) > 100:
            return False, f"{field_name} is too long (max 100 characters)"
        
        # Allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s'-]+$", name):
            return False, f"{field_name} contains invalid characters"
        
        return True, None


class PhoneValidator:
    """Validates phone numbers."""
    
    @staticmethod
    def validate(phone: str) -> Tuple[bool, Optional[str]]:
        """
        Validate phone number format.
        
        Args:
            phone: Phone number to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not phone or not isinstance(phone, str):
            return False, "Phone number is required"
        
        # Remove common phone number separators
        cleaned = re.sub(r'[\s\-().+]+', '', phone)
        
        # Check if valid length (international numbers are 7-15 digits)
        if len(cleaned) < 7 or len(cleaned) > 15:
            return False, "Phone number must be 7-15 digits"
        
        # Check if only digits and + at start
        if not re.match(r'^\+?[0-9]+$', cleaned):
            return False, "Phone number contains invalid characters"
        
        return True, None
