from flask import g
from flask_jwt_extended import get_jwt_identity

from users_companies.entity import UserCompanyEntity

from container import user_company_service


def _authz_del_request() -> tuple[UserCompanyEntity | None, set[str]]:
    if "current_authz" not in g:
        user_id = int(get_jwt_identity())
        g.current_authz = user_company_service.get_membership_with_permissions(user_id)

    return g.current_authz


def get_current_user_company() -> UserCompanyEntity | None:
    return _authz_del_request()[0]


def get_current_permissions() -> set[str]:
    return _authz_del_request()[1]
