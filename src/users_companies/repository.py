from sqlalchemy import select

from shared.database.base_repository import BaseRepository
from permissions.entity import PermissionsEntity
from role_permissions.entity import RolePermissionEntity
from users.entity import UserEntity

from .entity import UserCompanyEntity


class UserCompanyRepository(BaseRepository):

    def __init__(self):
        super().__init__(UserCompanyEntity)

    def get_membership_with_permissions(self, user_id: int) -> tuple[UserCompanyEntity | None, set[str]]:
        stmt = (
            select(UserCompanyEntity, PermissionsEntity.name)
            .outerjoin(RolePermissionEntity, RolePermissionEntity.role_id == UserCompanyEntity.role_id)
            .outerjoin(PermissionsEntity, PermissionsEntity.id == RolePermissionEntity.permission_id)
            .where(UserCompanyEntity.user_id == user_id)
        )
        filas = self.db.execute(stmt).all()
        if not filas:
            return None, set()

        return filas[0][0], {nombre for _, nombre in filas if nombre}

    def get_user_company_role_by_user_id(self, user_id: int) -> UserCompanyEntity | None:
        stmt = select(UserCompanyEntity).where(UserCompanyEntity.user_id == user_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_users_by_role_id(self, role_id: int) -> list[UserCompanyEntity]:
        stmt = select(UserCompanyEntity).where(UserCompanyEntity.role_id == role_id)
        return self.db.scalars(stmt).all()

    def get_users_with_role_by_company_id(self, company_id: int) -> list[tuple[UserEntity, int]]:
        stmt = (
            select(UserEntity, UserCompanyEntity.role_id)
            .join(UserCompanyEntity, UserCompanyEntity.user_id == UserEntity.id)
            .where(UserCompanyEntity.company_id == company_id)
            .order_by(UserEntity.id)
        )
        return self.db.execute(stmt).all()
