from sqlalchemy import select, func

from shared.database.base_repository import BaseRepository
from .entity import RoleEntity

class RoleRepository(BaseRepository):
    
    def __init__(self):
        super().__init__(RoleEntity)
    
    def get_roles_from_company_id(self, company_id: int, page: int, per_page: int) -> list[RoleEntity]:        
        total = self.db.scalar(select(func.count()).select_from(RoleEntity).where(RoleEntity.company_id == company_id))
        stmt = select(RoleEntity).where(RoleEntity.company_id == company_id).order_by(RoleEntity.id).offset((page - 1) * per_page).limit(per_page)
        roles = self.db.scalars(stmt).all()
        return roles, total

    def get_role_by_name(self, name: str, company_id: int) -> RoleEntity | None:
        stmt = select(RoleEntity).where(RoleEntity.name == name, RoleEntity.company_id == company_id)
        return self.db.execute(stmt).scalar_one_or_none()
