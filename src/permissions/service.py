from shared.service import BaseService

from .entity import PermissionsEntity
from .repository import PermissionRepository
from .model import (
    PermissionModel,
    CreatePermissionModel,
)
from .exceptions import PermissionAlreadyExists
from .interfaces import IPermissionService


class PermissionService(IPermissionService, BaseService):

    def __init__(self, permission_repo: PermissionRepository):
        self._permission_repo = permission_repo

    def get_all_permissions(self) -> list[dict]:
        permissions = self._permission_repo.get_all()
        return [PermissionModel.model_validate(permission).model_dump() for permission in permissions]

    def create_permission(self, data: dict):
        existing = self._permission_repo.get_permission_by_name(data["name"])
        if existing:
            raise PermissionAlreadyExists()

        permission_data = CreatePermissionModel.model_validate(data).model_dump()

        permission = PermissionsEntity(**permission_data)
        return self._permission_repo.create(permission)
