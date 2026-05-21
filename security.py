"""
Security middleware and utilities for the Student Registration System.
Provides security headers, CORS configuration, and XSS/CSRF protections.
"""

from flask import Flask
from flask_cors import CORS
from datetime import timedelta


def init_security(app: Flask) -> None:
    """
    Initialize all security features for the application.
    
    Args:
        app: Flask application instance
    """
    # CORS Configuration - Allow specific origins in production
    cors_config = {
        "origins": [
            "http://localhost:3000",
            "http://localhost:5000",
            "http://127.0.0.1:5000",
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 3600,
    }
    
    # Only use restricted CORS in production
    if app.config.get('ENV') == 'production':
        cors_config['origins'] = app.config.get('CORS_ORIGINS', [])
    
    CORS(app, resources={r"/api/*": cors_config})
    
    # Register security middleware
    app.after_request(add_security_headers)


def add_security_headers(response):
    """
    Add security headers to all responses.
    
    Headers included:
    - X-Frame-Options: DENY (prevents clickjacking)
    - X-Content-Type-Options: nosniff (prevents MIME sniffing)
    - X-XSS-Protection: 1; mode=block (enables browser XSS filter)
    - Strict-Transport-Security: enforces HTTPS
    - Content-Security-Policy: restricts resource loading
    - Referrer-Policy: controls referrer information
    - Permissions-Policy: controls browser features
    """
    
    # Prevent clickjacking attacks
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Enable XSS filter in older browsers
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Enforce HTTPS (set max-age to 31536000 = 1 year in production)
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    
    # Content Security Policy - restrict resources to same origin
    # Allow inline scripts for forms (replace with nonce in production)
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self';"
    )
    response.headers['Content-Security-Policy'] = csp
    
    # Control referrer information leaked in requests
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Disable access to browser features
    response.headers['Permissions-Policy'] = (
        'accelerometer=(), camera=(), geolocation=(), '
        'gyroscope=(), magnetometer=(), microphone=(), '
        'payment=(), usb=()'
    )
    
    return response


def get_session_config() -> dict:
    """
    Get Flask session configuration for security.
    
    Returns:
        Dictionary with session security settings
    """
    return {
        'SESSION_COOKIE_SECURE': True,      # HTTPS only
        'SESSION_COOKIE_HTTPONLY': True,    # JavaScript cannot access
        'SESSION_COOKIE_SAMESITE': 'Lax',   # CSRF protection
        'SESSION_COOKIE_NAME': '__Host-session',  # Prefix prevents subdomain access
        'PERMANENT_SESSION_LIFETIME': timedelta(hours=24),
        'SESSION_REFRESH_EACH_REQUEST': True,
    }
