
import functools
import hashlib
import json
import time
from flask import request, current_app

# Simple in-memory cache (for demonstration)
# In production, use Redis or another distributed cache system
cache_store = {}

def compute_cache_key():
    """Generate a cache key based on request path and query params."""
    cache_key = request.path
    args = request.args.copy()
    
    # Sort query parameters to ensure consistent cache keys
    if args:
        sorted_args = sorted(args.items())
        query_string = '&'.join(f"{k}={v}" for k, v in sorted_args)
        cache_key = f"{cache_key}?{query_string}"
        
    # Add authentication info if relevant
    # Simplified: In a real system, you'd include user-specific info
    auth_header = request.headers.get('Authorization', '')
    if auth_header:
        # Hash the auth info to avoid storing sensitive data in cache keys
        auth_hash = hashlib.md5(auth_header.encode()).hexdigest()
        cache_key = f"{cache_key}@{auth_hash}"
        
    return cache_key

def cache(timeout=300):
    """Cache decorator for API endpoints."""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # Only cache GET requests
            if request.method != 'GET':
                return f(*args, **kwargs)
                
            cache_key = compute_cache_key()
            
            # Check if result is in cache and not expired
            if cache_key in cache_store:
                result, expiry = cache_store[cache_key]
                if expiry > time.time():
                    return result
                    
            # Execute the function and cache the result
            result = f(*args, **kwargs)
            expiry = time.time() + timeout
            cache_store[cache_key] = (result, expiry)
            
            return result
        return wrapper
    return decorator

def invalidate_cache_for_user(user_id):
    """Invalidate all cache entries for a specific user."""
    # In a real system, you'd have more sophisticated cache invalidation
    # This is a simplified approach
    user_specific_keys = []
    for key in cache_store.keys():
        if f"user_id={user_id}" in key or f"@{user_id}" in key:
            user_specific_keys.append(key)
            
    for key in user_specific_keys:
        if key in cache_store:
            del cache_store[key]

def invalidate_cache_for_website(website_id):
    """Invalidate all cache entries for a specific website."""
    website_specific_keys = []
    for key in cache_store.keys():
        if website_id in key:
            website_specific_keys.append(key)
            
    for key in website_specific_keys:
        if key in cache_store:
            del cache_store[key]