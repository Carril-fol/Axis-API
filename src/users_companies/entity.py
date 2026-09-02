from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from shared.database.database import Base
from users.entity import UserEntity
from roles.entity import RoleEntity
from companies.entity import CompanyEntity


class UserCompanyEntity(Base):
    __tablename__ = "users_companies"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False, index=True)
    
    roles = relationship(RoleEntity)
    users = relationship(UserEntity)
    companies = relationship(CompanyEntity)
