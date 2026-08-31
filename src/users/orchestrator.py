from companies.interfaces import ICompanyService
from role_permissions.interfaces import IRolePermissionService
from roles.interfaces import IRoleService
from users_companies.interfaces import IUserCompanyService

from .interfaces import IUserService
from .exceptions import UserWithAnEmailAlreadyExists


class UserRegistrationOrchestrator:

    def __init__(
        self,
        user_service: IUserService,
        company_service: ICompanyService,
        role_service: IRoleService,
        role_permission_service: IRolePermissionService,
        user_company_service: IUserCompanyService,
    ):
        self._user_service = user_service
        self._company_service = company_service
        self._role_service = role_service
        self._role_permission_service = role_permission_service
        self._user_company_service = user_company_service

    def register_owner(self, user_data: dict, company_data: dict) -> int:
        if self._user_service.get_user_by_email(user_data["email"]):
            raise UserWithAnEmailAlreadyExists()

        user = self._user_service.create_user(user_data)
        company = self._company_service.create_company(company_data)

        role_id = self._role_service.ensure_owner_role(company.id)
        self._role_permission_service.grant_all_permissions(role_id)

        self._user_company_service.create_membership(user.id, role_id, company.id)

        return user.id
