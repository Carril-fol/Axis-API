from sqlalchemy import Column, Index, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from shared.database.database import Base
from roles.entity import RoleEntity
from permissions.entity import PermissionsEntity

class RolePermissionEntity(Base):
    __tablename__ = "role_permission"
    id = Column(Integer, primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    permissions = relationship(PermissionsEntity)
    roles = relationship(RoleEntity)


Index(
    "ix_role_permission_role_permission",
    RolePermissionEntity.role_id,
    RolePermissionEntity.permission_id,
    unique=True,
)
