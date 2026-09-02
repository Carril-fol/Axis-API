from shared.service import BaseService

from users.interfaces import IUserService
from .model import RegisterInputFromCompany

from roles.interfaces import IRoleService

from .interfaces import IUserCompanyService
from .repository import UserCompanyRepository
from .entity import UserCompanyEntity
from .model import CreateUserCompanyModel, UserFromCompanyModel
from .exceptions import (
    UserWithAnEmailAlreadyExists,
    UserCompanyInsufficientRolePrivileges,
    UserCompanyNotFound
)


class UserCompanyService(IUserCompanyService, BaseService):
    
    def __init__(
        self,
        user_service: IUserService,
        role_service: IRoleService,
        user_company_repo: UserCompanyRepository
    ):
        self.user_service = user_service
        self.role_service = role_service
        self.user_company_repo = user_company_repo

    def _validate_role_action(self, user_id: int, requesting_user_id: int) -> UserCompanyEntity:
        target_user_role = self.user_company_repo.get_user_company_role_by_user_id(user_id)
        if target_user_role is None:
            raise UserCompanyNotFound()

        requesting_user_role = self.user_company_repo.get_user_company_role_by_user_id(requesting_user_id)

        if target_user_role.role_id == requesting_user_role.role_id:
            raise UserCompanyInsufficientRolePrivileges()

        if self.role_service.is_role_owner(target_user_role.role_id):
            raise UserCompanyInsufficientRolePrivileges()

        return target_user_role

    def create_user_for_company(self, data: RegisterInputFromCompany, company_id: int) -> None:
        if self.user_service.get_user_by_email(data.email):
            raise UserWithAnEmailAlreadyExists()

        user_created = self.user_service.create_user(data.model_dump(exclude={"role_id"}))
        self.create_membership(user_created.id, data.role_id, company_id)

    def update_user_from_company(self, user_id: int, data: dict, requesting_user_id: int):
        self._validate_role_action(user_id, requesting_user_id)
        return self.user_service.update_user(user_id, data)

    def delete_user_from_company(self, user_id: int, requesting_user_id: int):
        target_user_role = self._validate_role_action(user_id, requesting_user_id)
        self.user_company_repo.delete(target_user_role)
        return self.user_service.delete_user(user_id)

    def get_users_from_company(self, company_id: int) -> list[dict]:
        rows = self.user_company_repo.get_users_with_role_by_company_id(company_id)
        return [
            UserFromCompanyModel(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                date_creation=user.date_creation,
                role_id=role_id,
            ).model_dump()
            for user, role_id in rows
        ]

    def create_membership(self, user_id: int, role_id: int, company_id: int) -> UserCompanyEntity:
        membership = CreateUserCompanyModel.model_validate(
            {"user_id": user_id, "role_id": role_id, "company_id": company_id}
        ).model_dump()
        return self.user_company_repo.create(UserCompanyEntity(**membership))

    def get_membership_with_permissions(self, user_id: int) -> tuple[UserCompanyEntity | None, set[str]]:
        return self.user_company_repo.get_membership_with_permissions(user_id)

    def get_membership_by_user_id(self, user_id: int) -> UserCompanyEntity | None:
        return self.user_company_repo.get_user_company_role_by_user_id(user_id)

    def get_memberships_by_role_id(self, role_id: int) -> list[UserCompanyEntity]:
        return self.user_company_repo.get_users_by_role_id(role_id)

    def update_membership(self, membership: UserCompanyEntity) -> UserCompanyEntity:
        return self.user_company_repo.update(membership)
