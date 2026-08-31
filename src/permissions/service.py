from shared.service import BaseService

from .entity import PermissionsEntity
from .repository import PermissionRepository
from .model import (
    PermissionModel,
    CreatePermissionModel,
)
from .exceptions import (
    PermissionNotFound, 
    PermissionAlreadyExists
)
from .interfaces import IPermissionService


class PermissionService(IPermissionService, BaseService):

    def __init__(self, permission_repo: PermissionRepository):
        self._permission_repo = permission_repo

    def _get_permission_by_name_or_raise(self, name: str) -> PermissionsEntity:
        permission = self._permission_repo.get_permission_by_name(name.upper())
        if not permission:
            raise PermissionNotFound()
        return permission

    def get_permission_by_name(self, name: str) -> dict:
        permission = self._get_permission_by_name_or_raise(name)
        return PermissionModel.model_validate(permission).model_dump()

    def get_all_permissions(self) -> list[dict]:
        permissions = self._permission_repo.get_all()
        return [PermissionModel.model_validate(permission).model_dump() for permission in permissions]

    def create_permission(self, data: dict):
        normalized_name = data["name"].upper()
        
        existing = self._permission_repo.get_permission_by_name(normalized_name)
        if existing:
            raise PermissionAlreadyExists()

        permission_data = CreatePermissionModel.model_validate(data).model_dump()

        permission = PermissionsEntity(**permission_data)
        return self._permission_repo.create(permission)