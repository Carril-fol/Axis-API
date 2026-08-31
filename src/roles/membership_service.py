from shared.service import BaseService

from users_companies.interfaces import IUserCompanyService

from .interfaces import IRoleService
from .exceptions import RoleNotFound, UserNotInCompany


class RoleMembershipService(BaseService):

    def __init__(self, role_service: IRoleService, user_company_service: IUserCompanyService):
        self._role_service = role_service
        self._user_company_service = user_company_service

    def delete_role_and_reassign_members(self, role_id: int, company_id: int, data: dict):
        role_deleted = self._role_service.delete_soft_rol(role_id, data)
        self._reassign_members_to_default(role_id, company_id)
        return role_deleted

    def assign_role_to_user(self, user_id: int, role_id: int, company_id: int):
        membership = self._user_company_service.get_membership_by_user_id(user_id)
        if not membership or membership.company_id != company_id:
            raise UserNotInCompany()

        role = self._role_service.get_role_by_id(role_id)
        if role["company_id"] != company_id:
            raise RoleNotFound()

        membership_updated = self._update_instance_entity({"role_id": role_id}, membership)
        return self._user_company_service.update_membership(membership_updated)

    def _reassign_members_to_default(self, role_id: int, company_id: int) -> None:
        affected = self._user_company_service.get_memberships_by_role_id(role_id)
        if not affected:
            return

        default_role_id = self._role_service.ensure_default_role(company_id)
        for membership in affected:
            updated = self._update_instance_entity({"role_id": default_role_id}, membership)
            self._user_company_service.update_membership(updated)
