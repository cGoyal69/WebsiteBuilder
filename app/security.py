import time
import functools
import uuid
from flask import request, jsonify, session
from hmac import compare_digest as safe_str_cmp

# In-memory rate limiter (replace with Redis in production)
rate_limiter = {}

def rate_limit(requests_per_minute=60):
    """Decorator for rate limiting API endpoints."""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            client_id = request.remote_addr or "anonymous"
            
            now = time.time()
            limiter = rate_limiter.setdefault(client_id, {'requests': 0, 'reset_time': now + 60})

            if now > limiter['reset_time']:
                limiter['requests'] = 0
                limiter['reset_time'] = now + 60

            limiter['requests'] += 1

            if limiter['requests'] > requests_per_minute:
                return jsonify({'message': 'Rate limit exceeded. Try again later.'}), 429

            return f(*args, **kwargs)
        return wrapper
    return decorator

# CSRF Protection (simple demo version)
def generate_csrf_token():
    """Generate a CSRF token."""
    token = str(uuid.uuid4())
    session['csrf_token'] = token
    return token

def validate_csrf_token(token):
    """Validate CSRF token from session."""
    return safe_str_cmp(token, session.get('csrf_token', '')) if token else False

# Website Data Validation
def validate_website_data(data):
    """Validate website creation/update data."""
    required_fields = ['name']
    errors = []

    for field in required_fields:
        if field not in data or not isinstance(data[field], str) or not data[field].strip():
            errors.append(f"Missing or invalid required field: {field}")

    string_fields = ['name', 'business_type', 'industry', 'template', 'description', 'location', 'logo_tagline']
    for field in string_fields:
        if field in data and not isinstance(data[field], str):
            errors.append(f"Field '{field}' must be a string")

    return errors

# Security Headers Middleware
def add_security_headers(response):
    """Add essential security headers."""
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "img-src 'self' data: /api/placeholder/; "
        "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
        "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com"
    )
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response