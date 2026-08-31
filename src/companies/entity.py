from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from shared.database.database import Base


class CompanyEntity(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    address = Column(String, nullable=False)
    date_creation = Column(DateTime, nullable=False, default=datetime.now)