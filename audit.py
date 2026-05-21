"""
Audit logging utilities for the Student Registration System.
Provides structured logging, user action tracking, and request/response logging middleware.
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from functools import wraps

from flask import request, g, has_request_context


class StructuredLogger:
    """Handles structured JSON logging for audit trails."""
    
    def __init__(self, name: str):
        """
        Initialize structured logger.
        
        Args:
            name: Logger name (usually __name__)
        """
        self.logger = logging.getLogger(name)
        self._setup_handler()
    
    def _setup_handler(self) -> None:
        """Setup JSON formatter for the logger."""
        # Create console handler with JSON formatting
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        
        # Only add handler if not already present
        if not any(isinstance(h, logging.StreamHandler) for h in self.logger.handlers):
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def log_event(
        self,
        event_type: str,
        message: str,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        severity: str = "INFO",
    ) -> None:
        """
        Log a structured event.
        
        Args:
            event_type: Type of event (e.g., 'AUTH_LOGIN', 'USER_CREATED')
            message: Human-readable message
            user_id: User performing the action
            details: Additional details as dictionary
            severity: Log level ('INFO', 'WARNING', 'ERROR', 'CRITICAL')
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'message': message,
            'user_id': user_id or 'SYSTEM',
            'details': details or {},
        }
        
        # Add request context if available
        if has_request_context():
            log_entry['request_id'] = g.get('request_id', 'N/A')
            log_entry['ip_address'] = request.remote_addr
            log_entry['method'] = request.method
            log_entry['path'] = request.path
        
        # Log with appropriate severity
        severity_map = {
            'INFO': self.logger.info,
            'WARNING': self.logger.warning,
            'ERROR': self.logger.error,
            'CRITICAL': self.logger.critical,
        }
        
        log_func = severity_map.get(severity, self.logger.info)
        log_func(json.dumps(log_entry))
    
    def log_auth_event(
        self,
        action: str,
        user_id: str,
        success: bool,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log authentication-related events.
        
        Args:
            action: Auth action ('LOGIN', 'LOGOUT', 'PASSWORD_RESET', 'MFA')
            user_id: User ID
            success: Whether action succeeded
            details: Additional context
        """
        message = f"Authentication {action}: {'SUCCESS' if success else 'FAILED'}"
        severity = "INFO" if success else "WARNING"
        
        self.log_event(
            event_type=f"AUTH_{action}",
            message=message,
            user_id=user_id,
            details=details,
            severity=severity,
        )
    
    def log_data_change(
        self,
        action: str,
        entity_type: str,
        entity_id: str,
        user_id: str,
        old_values: Optional[Dict] = None,
        new_values: Optional[Dict] = None,
    ) -> None:
        """
        Log data modification events.
        
        Args:
            action: Type of change ('CREATE', 'UPDATE', 'DELETE')
            entity_type: Type of entity (e.g., 'STUDENT', 'ADMIN')
            entity_id: ID of entity
            user_id: User making the change
            old_values: Previous values (for UPDATE/DELETE)
            new_values: New values (for CREATE/UPDATE)
        """
        message = f"{action} {entity_type}: {entity_id}"
        
        details = {
            'action': action,
            'entity_type': entity_type,
            'entity_id': entity_id,
        }
        
        if old_values:
            details['old_values'] = old_values
        if new_values:
            details['new_values'] = new_values
        
        self.log_event(
            event_type=f"DATA_{action}",
            message=message,
            user_id=user_id,
            details=details,
        )
    
    def log_access(
        self,
        resource: str,
        action: str,
        user_id: Optional[str],
        granted: bool,
        reason: Optional[str] = None,
    ) -> None:
        """
        Log resource access attempts.
        
        Args:
            resource: Resource being accessed
            action: Type of access ('READ', 'WRITE', 'DELETE')
            user_id: User attempting access
            granted: Whether access was granted
            reason: Reason if denied
        """
        severity = "INFO" if granted else "WARNING"
        message = f"Access {'GRANTED' if granted else 'DENIED'}: {action} on {resource}"
        
        details = {
            'resource': resource,
            'action': action,
            'granted': granted,
        }
        
        if reason:
            details['reason'] = reason
        
        self.log_event(
            event_type="ACCESS_CONTROL",
            message=message,
            user_id=user_id,
            details=details,
            severity=severity,
        )


class JsonFormatter(logging.Formatter):
    """Custom formatter that outputs structured JSON logs."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        if isinstance(record.msg, str) and record.msg.startswith('{'):
            # Message is already JSON
            return record.msg
        
        # Create log entry
        log_entry = {
            'timestamp': datetime.utcfromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)


def log_request_response(f):
    """
    Decorator to log HTTP requests and responses.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Generate request ID
        request_id = str(uuid.uuid4())
        g.request_id = request_id
        
        # Log incoming request
        logger = StructuredLogger(__name__)
        
        request_details = {
            'request_id': request_id,
            'method': request.method,
            'path': request.path,
            'content_type': request.content_type,
            'user_agent': request.headers.get('User-Agent', 'Unknown'),
        }
        
        # Log request parameters (be careful with sensitive data)
        if request.method == 'GET':
            request_details['query_params'] = request.args.to_dict()
        elif request.method in ['POST', 'PUT', 'PATCH']:
            try:
                request_details['body_type'] = type(request.get_json()).__name__
            except:
                pass
        
        logger.log_event(
            event_type="HTTP_REQUEST",
            message=f"{request.method} {request.path}",
            details=request_details,
        )
        
        # Execute the route handler
        try:
            response = f(*args, **kwargs)
            status_code = response[1] if isinstance(response, tuple) else 200
            
            logger.log_event(
                event_type="HTTP_RESPONSE",
                message=f"{request.method} {request.path} -> {status_code}",
                details={
                    'request_id': request_id,
                    'status_code': status_code,
                    'method': request.method,
                    'path': request.path,
                },
            )
            
            # Add request ID to response headers
            if isinstance(response, tuple):
                response_obj = response[0]
                if hasattr(response_obj, 'headers'):
                    response_obj.headers['X-Request-ID'] = request_id
            
            return response
        except Exception as e:
            logger.log_event(
                event_type="HTTP_ERROR",
                message=f"Error handling {request.method} {request.path}: {str(e)}",
                details={
                    'request_id': request_id,
                    'error': str(e),
                    'error_type': type(e).__name__,
                },
                severity="ERROR",
            )
            raise
    
    return decorated_function


class AuditLog:
    """Convenience class for accessing the audit logger."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = StructuredLogger(__name__)
        return cls._instance
    
    @staticmethod
    def get_logger() -> StructuredLogger:
        """Get the singleton audit logger instance."""
        if AuditLog._instance is None:
            AuditLog._instance = StructuredLogger(__name__)
        return AuditLog._instance
