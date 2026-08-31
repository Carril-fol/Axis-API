from sqlalchemy import select

from shared.database.base_repository import BaseRepository
from permissions.entity import PermissionsEntity

from .entity import RolePermissionEntity


class RolePermissionsRepository(BaseRepository):

    def __init__(self):
        super().__init__(RolePermissionEntity)

    def get_role_permission(self, role_id: int, permission_id: int) -> RolePermissionEntity | None:
        stmt = select(RolePermissionEntity).where(
            RolePermissionEntity.role_id == role_id, 
            RolePermissionEntity.permission_id == permission_id
        )
        return self.db.execute(stmt).scalar_one_or_none()
    
    def get_all_permissions_by_role_id(self, role_id: int):
        stmt = select(PermissionsEntity).join(
            RolePermissionEntity, 
            PermissionsEntity.id == RolePermissionEntity.permission_id
        ).where(RolePermissionEntity.role_id == role_id)
        
        return self.db.scalars(stmt).all()