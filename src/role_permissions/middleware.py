from functools import wraps
from flask_jwt_extended import verify_jwt_in_request

from shared.authz import get_current_permissions, get_current_user_company


def require_permission(permission: str):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            if get_current_user_company() is None:
                return {"error": "Forbidden"}, 403

            if permission not in get_current_permissions():
                return {"error": "Forbidden"}, 403

            return f(*args, **kwargs)
        return wrapper
    return decorator
