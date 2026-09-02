from sqlalchemy import select

from shared.database.base_repository import BaseRepository
from .entity import UserEntity


class UserRepository(BaseRepository):

    def __init__(self):
        super().__init__(UserEntity)

    def get_user_by_email(self, email: str) -> UserEntity | None:
        stmt = select(UserEntity).where(UserEntity.email == email)
        return self.db.execute(stmt).scalar_one_or_none()
