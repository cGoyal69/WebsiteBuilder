
from flask import request, jsonify, current_app
import time
import functools
import redis
from hmac import compare_digest as safe_str_cmp
import uuid

# Rate limiting using a simple in-memory store (for demonstration)
# In production, use Redis or another distributed store
rate_limiter = {}

def rate_limit(requests_per_minute=60):
    """Decorator for rate limiting API endpoints."""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # Get client identifier (IP address or token if authenticated)
            client_id = request.remote_addr
            
            # Check if client has a rate limit entry
            if client_id not in rate_limiter:
                rate_limiter[client_id] = {
                    'requests': 0,
                    'reset_time': time.time() + 60
                }
            
            # Check if reset time has passed
            if time.time() > rate_limiter[client_id]['reset_time']:
                rate_limiter[client_id]['requests'] = 0
                rate_limiter[client_id]['reset_time'] = time.time() + 60
            
            # Increment request count
            rate_limiter[client_id]['requests'] += 1
            
            # Check if rate limit exceeded
            if rate_limiter[client_id]['requests'] > requests_per_minute:
                return jsonify({
                    'message': 'Rate limit exceeded. Try again later.'
                }), 429
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

# CSRF Protection
def generate_csrf_token():
    """Generate a CSRF token."""
    return str(uuid.uuid4())

def validate_csrf_token(token):
    """Validate CSRF token from session."""
    # In a real app, you'd compare with a token stored in session
    # This is a simplified version
    return len(token) > 10  # Basic validation for demonstration

# Input Validation
def validate_website_data(data):
    """Validate website data."""
    required_fields = ['name']
    errors = []
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Validate string fields
    string_fields = ['name', 'business_type', 'industry', 'template']
    for field in string_fields:
        if field in data and not isinstance(data[field], str):
            errors.append(f"Field {field} must be a string")
    
    # Additional validation as needed...
    
    return errors

# Content Security Policy
def add_security_headers(response):
    """Add security headers to response."""
    response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' /api/placeholder/; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com;"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response