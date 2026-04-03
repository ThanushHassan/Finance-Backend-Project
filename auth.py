from functools import wraps
from flask import request, jsonify

def role_required(allowed_roles):
    """
    Decorator to restrict access based on the 'X-User-Role' header.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check for the custom header
            user_role = request.headers.get('X-User-Role') 
            
            if not user_role:
                return jsonify({"error": "Authentication required. Missing X-User-Role header."}), 401
            
            if user_role not in allowed_roles:
                return jsonify({"error": f"Access denied. {user_role} role cannot perform this action."}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator