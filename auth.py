"""
Authentication utilities for the Student Registration System.
Provides JWT token generation/validation, password hashing, and OAuth2 skeleton.
"""

from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, Tuple, Optional

import jwt
from flask import current_app, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


class TokenManager:
    """Manages JWT token generation, validation, and refresh."""
    
    @staticmethod
    def generate_tokens(user_id: str, username: str, is_admin: bool = False) -> Dict[str, str]:
        """
        Generate access and refresh tokens for a user.
        
        Args:
            user_id: Unique user identifier
            username: Username for token payload
            is_admin: Whether user has admin privileges
            
        Returns:
            Dictionary with 'access_token' and 'refresh_token'
        """
        now = datetime.utcnow()
        access_expires = now + timedelta(hours=1)
        refresh_expires = now + timedelta(days=7)
        
        access_payload = {
            'user_id': user_id,
            'username': username,
            'is_admin': is_admin,
            'type': 'access',
            'iat': now,
            'exp': access_expires,
        }
        
        refresh_payload = {
            'user_id': user_id,
            'username': username,
            'type': 'refresh',
            'iat': now,
            'exp': refresh_expires,
        }
        
        access_token = jwt.encode(
            access_payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        
        refresh_token = jwt.encode(
            refresh_payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': 3600,  # 1 hour in seconds
        }
    
    @staticmethod
    def validate_token(token: str, token_type: str = 'access') -> Optional[Dict]:
        """
        Validate JWT token and return payload.
        
        Args:
            token: JWT token string
            token_type: Expected token type ('access' or 'refresh')
            
        Returns:
            Token payload if valid, None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            
            # Verify token type
            if payload.get('type') != token_type:
                return None
                
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def refresh_token(refresh_token: str) -> Optional[Dict[str, str]]:
        """
        Generate new access token from refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            Dictionary with new 'access_token' if valid, None otherwise
        """
        payload = TokenManager.validate_token(refresh_token, token_type='refresh')
        
        if not payload:
            return None
        
        # Generate new access token
        new_tokens = TokenManager.generate_tokens(
            payload['user_id'],
            payload['username'],
            payload.get('is_admin', False)
        )
        
        return new_tokens


class PasswordManager:
    """Handles password hashing and verification."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using werkzeug.security.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password to verify
            hashed: Previously hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        return check_password_hash(hashed, password)


def token_required(f):
    """
    Decorator to require valid JWT token for route access.
    Validates Bearer token in Authorization header.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # "Bearer <token>"
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        payload = TokenManager.validate_token(token, token_type='access')
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Attach payload to request context
        request.user_id = payload['user_id']
        request.username = payload['username']
        request.is_admin = payload.get('is_admin', False)
        
        return f(*args, **kwargs)
    
    return decorated_function


def admin_required(f):
    """
    Decorator to require admin privileges.
    Must be used after @token_required.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(request, 'is_admin') or not request.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


class OAuth2Config:
    """Skeleton for OAuth2 provider configuration."""
    
    GOOGLE_OAUTH_CONFIG = {
        'client_id': None,  # Set from environment
        'client_secret': None,  # Set from environment
        'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        'token_url': 'https://accounts.google.com/o/oauth2/token',
        'userinfo_url': 'https://www.googleapis.com/oauth2/v1/userinfo',
        'scopes': ['openid', 'email', 'profile'],
    }
    
    GITHUB_OAUTH_CONFIG = {
        'client_id': None,  # Set from environment
        'client_secret': None,  # Set from environment
        'authorize_url': 'https://github.com/login/oauth/authorize',
        'token_url': 'https://github.com/login/oauth/access_token',
        'userinfo_url': 'https://api.github.com/user',
        'scopes': ['user:email'],
    }
    
    @staticmethod
    def load_from_env():
        """Load OAuth2 credentials from environment variables."""
        import os
        
        OAuth2Config.GOOGLE_OAUTH_CONFIG['client_id'] = os.environ.get('GOOGLE_CLIENT_ID')
        OAuth2Config.GOOGLE_OAUTH_CONFIG['client_secret'] = os.environ.get('GOOGLE_CLIENT_SECRET')
        
        OAuth2Config.GITHUB_OAUTH_CONFIG['client_id'] = os.environ.get('GITHUB_CLIENT_ID')
        OAuth2Config.GITHUB_OAUTH_CONFIG['client_secret'] = os.environ.get('GITHUB_CLIENT_SECRET')
