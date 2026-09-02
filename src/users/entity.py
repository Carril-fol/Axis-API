from shared.database.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime


class UserEntity(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    date_creation = Column(DateTime, nullable=False, default=datetime.now)
