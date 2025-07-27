import logging
import os
from datetime import datetime
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from collections import defaultdict
import time
import re

# Configure logging for request logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler('requests.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

User = get_user_model()


class RequestLoggingMiddleware:
    """
    Middleware that logs each user's requests to a file, including timestamp, user, and request path.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Get user information
        user = request.user if request.user.is_authenticated else "Anonymous"
        
        # Log the request information
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        # Process the request
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app during certain hours of the day.
    Access is restricted outside 6 AM to 9 PM.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Get current hour (24-hour format)
        current_hour = datetime.now().hour
        
        # Check if current time is outside allowed hours (6 AM to 9 PM)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "Access to the messaging app is restricted outside 6 AM to 9 PM. "
                f"Current time: {datetime.now().strftime('%H:%M')}"
            )
        
        # Process the request if within allowed hours
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware that limits the number of chat messages a user can send within a certain time window,
    based on their IP address. Limits to 5 messages per minute.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track message counts per IP
        self.ip_message_counts = defaultdict(list)
        self.rate_limit = 5  # messages per minute
        self.time_window = 60  # 60 seconds
        
    def __call__(self, request):
        # Only apply rate limiting to POST requests (new messages)
        if request.method == 'POST' and '/api/messages/' in request.path:
            client_ip = self.get_client_ip(request)
            current_time = time.time()
            
            # Clean old entries (older than time window)
            self.ip_message_counts[client_ip] = [
                timestamp for timestamp in self.ip_message_counts[client_ip]
                if current_time - timestamp < self.time_window
            ]
            
            # Check if rate limit exceeded
            if len(self.ip_message_counts[client_ip]) >= self.rate_limit:
                return HttpResponseForbidden(
                    f"Rate limit exceeded. You can only send {self.rate_limit} messages per minute. "
                    f"Please wait before sending another message."
                )
            
            # Add current timestamp
            self.ip_message_counts[client_ip].append(current_time)
        
        # Process the request
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get the client's IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware:
    """
    Middleware that checks the user's role before allowing access to specific actions.
    Only admin and moderator users are allowed access.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Define protected paths that require admin/moderator access
        protected_paths = [
            '/admin/',
            '/api/users/',
            '/api/conversations/',
        ]
        
        # Check if the request path requires role-based access control
        requires_role_check = any(request.path.startswith(path) for path in protected_paths)
        
        if requires_role_check:
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required for this action.")
            
            # Check if user has the required role
            user_role = getattr(request.user, 'role', None)
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden(
                    f"Access denied. Required role: admin or moderator. "
                    f"Your role: {user_role or 'none'}"
                )
        
        # Process the request
        response = self.get_response(request)
        return response
