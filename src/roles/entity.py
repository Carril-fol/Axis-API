from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from shared.database.database import Base
from companies.entity import CompanyEntity


class RoleEntity(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    companies = relationship(CompanyEntity)
