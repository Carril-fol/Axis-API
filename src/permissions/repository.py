from sqlalchemy import select

from shared.database.base_repository import BaseRepository
from .entity import PermissionsEntity


class PermissionRepository(BaseRepository):
    
    def __init__(self):
        super().__init__(PermissionsEntity)
    
    def get_permission_by_name(self, name: str) -> PermissionsEntity | None:
        stmt = select(PermissionsEntity).where(PermissionsEntity.name == name)
        return self.db.execute(stmt).scalar_one_or_none()
