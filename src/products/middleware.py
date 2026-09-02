from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request

from shared.authz import get_current_user_company

from container import product_repository

def require_user_from_same_company():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            product_id_url = kwargs.get("id")

            product = product_repository.get_by_id(product_id_url)
            if product is None:
                return jsonify({"error": "Product not found"}), 404

            current_user_company = get_current_user_company()
            if current_user_company.company_id != product.company_id:
                return jsonify({"error": "Access denied to this company"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
