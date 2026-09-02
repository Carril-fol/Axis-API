from sqlalchemy import Column, Integer, String

from shared.database.database import Base


class PermissionsEntity(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
