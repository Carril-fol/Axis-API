from shared.service import BaseService

from permissions.interfaces import IPermissionService

from roles.interfaces import IRoleService
from roles.exceptions import RoleNotFound

from .repository import RolePermissionsRepository
from .entity import RolePermissionEntity
from .model import (
    AssignRolePermissionModel,
    UpdateRolePermissionModel
)
from .exceptions import (
    RoleNotInCompany, 
    RolePermissionNotFound, 
    RolePermissionsAlreadyHasAPermission
)
from .interfaces import IRolePermissionService


class RolePermissionService(IRolePermissionService, BaseService):
    
    def __init__(
        self,
        role_permission_repo: RolePermissionsRepository,
        role_service: IRoleService,
        permission_service: IPermissionService
    ):
        self._role_permission_repo = role_permission_repo
        self._role_service = role_service
        self._permission_service = permission_service

    def _get_role_permission_by_id(self, id: int):
        return self._role_permission_repo.get_by_id(id)

    def _get_role_or_raise(self, role_id: int):
        role = self._role_service.get_role_by_id(role_id)
        if not role:
            raise RoleNotFound()
        return role

    def _get_role_in_company_or_raise(self, role_id: int, company_id: int) -> dict:
        role = self._get_role_or_raise(role_id)
        if role["company_id"] != company_id:
            raise RoleNotInCompany()
        return role

    def assign_role_permission(self, data: dict, company_id: int):
        assign_role_permission = AssignRolePermissionModel.model_validate(data)
        role = self._get_role_in_company_or_raise(assign_role_permission.role_id, company_id)

        permission_ids = assign_role_permission.permission_id

        for permission_id in permission_ids:
            if self._role_permission_repo.get_role_permission(role["id"], permission_id):
                raise RolePermissionsAlreadyHasAPermission()

        for permission_id in permission_ids:
            role_permission = RolePermissionEntity(role_id=role["id"], permission_id=permission_id)
            self._role_permission_repo.create(role_permission)

    def grant_all_permissions(self, role_id: int) -> None:
        for permission in self._permission_service.get_all_permissions():
            if self._role_permission_repo.get_role_permission(role_id, permission["id"]):
                continue

            self._role_permission_repo.create(
                RolePermissionEntity(role_id=role_id, permission_id=permission["id"])
            )

    def update_role_permission(self, id: int, data: dict, company_id: int):
        role_permission = self._get_role_permission_by_id(id)
        if not role_permission:
            raise RolePermissionNotFound()

        self._get_role_in_company_or_raise(role_permission.role_id, company_id)
        
        data_validated = UpdateRolePermissionModel.model_validate(data).model_dump()
        new_role_id = data_validated["role_id"]
        new_permission_id = data_validated["permission_id"]

        if new_role_id != role_permission.role_id:
            self._get_role_in_company_or_raise(new_role_id, company_id)
        
        duplicated = self._role_permission_repo.get_role_permission(new_role_id, new_permission_id)
        if duplicated and duplicated.id != role_permission.id:
            raise RolePermissionsAlreadyHasAPermission()
        
        role_permission_updated = self._update_instance_entity(data_validated, role_permission)
        return self._role_permission_repo.update(role_permission_updated)
    
    def list_permissions_by_role_id(self, role_id: int, company_id: int) -> list[str]:
        role = self._get_role_in_company_or_raise(role_id, company_id)
        return [permission.name for permission in self._role_permission_repo.get_all_permissions_by_role_id(role["id"])]

    def revoke_permission(self, role_id: int, permission_id: int, company_id: int):
        role = self._get_role_in_company_or_raise(role_id, company_id)
        
        link = self._role_permission_repo.get_role_permission(role["id"], permission_id)
        if not link:
            raise RolePermissionNotFound()
        
        return self._role_permission_repo.delete(link)
