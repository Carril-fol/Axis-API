from shared.database.database import Base

from companies.entity import CompanyEntity
from categories.entity import CategoryEntity

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class ProductEntity(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, unique=False)
    date_creation = Column(DateTime, nullable=False, default=datetime.now)
    date_updated = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False, index=True)

    category = relationship(CategoryEntity)
    companies = relationship(CompanyEntity)
