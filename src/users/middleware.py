from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
from shared.authz import get_current_user_company

from container import user_company_repository as users_companies_repository

def require_user_from_same_company():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            user_id_url = kwargs.get("id")
            if not user_id_url:
                return {"error": "User ID not found in request"}, 400

            current_user_company = get_current_user_company()
            target_user_company = users_companies_repository.get_user_company_role_by_user_id(user_id_url)

            if not target_user_company:
                return {"error": "User not found"}, 404

            if current_user_company.company_id != target_user_company.company_id:
                return {"error": "Access denied to this company"}, 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator

