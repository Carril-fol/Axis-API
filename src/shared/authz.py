from functools import wraps

from flask import g
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from users_companies.entity import UserCompanyEntity
from users_companies.exceptions import UserCompanyNotFound

from container import (
    product_service,
    role_service,
    stock_service,
    user_company_service,
)


def _authz_del_request() -> tuple[UserCompanyEntity | None, set[str]]:
    if "current_authz" not in g:
        user_id = int(get_jwt_identity())
        g.current_authz = user_company_service.get_membership_with_permissions(user_id)

    return g.current_authz


def get_current_user_company() -> UserCompanyEntity | None:
    return _authz_del_request()[0]


def get_current_permissions() -> set[str]:
    return _authz_del_request()[1]


def require_permission(permission: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            if get_current_user_company() is None:
                return {"error": "Forbidden"}, 403

            if permission not in get_current_permissions():
                return {"error": "Forbidden"}, 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def require_same_company(resolve_company_id):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            current_user_company = get_current_user_company()
            if current_user_company is None:
                return {"error": "Forbidden"}, 403

            if current_user_company.company_id != resolve_company_id(kwargs["id"]):
                return {"error": "Access denied to this company"}, 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def _product_company_id(id: int) -> int:
    return product_service.get_product_by_id(id)["company_id"]


def _role_company_id(id: int) -> int:
    return role_service.get_role_by_id(id)["company_id"]


def _stock_company_id(id: int) -> int:
    return stock_service.get_stock_by_id(id)["product"]["company_id"]


def _user_company_id(id: int) -> int:
    membership = user_company_service.get_membership_by_user_id(id)
    if membership is None:
        raise UserCompanyNotFound()
    return membership.company_id


require_product_from_same_company = require_same_company(_product_company_id)
require_role_from_same_company = require_same_company(_role_company_id)
require_stock_from_same_company = require_same_company(_stock_company_id)
require_user_from_same_company = require_same_company(_user_company_id)
