from sqlalchemy import select

from shared.database.base_repository import BaseRepository
from .entity import UserEntity


class UserRepository(BaseRepository):

    def __init__(self):
        super().__init__(UserEntity)

    def create_user(self, user: UserEntity) -> UserEntity:
        return self.create(user)

    def update_user(self, user: UserEntity) -> UserEntity:
        return self.update(user)

    def delete_user(self, user: UserEntity) -> None:
        return self.delete(user)

    def get_user_by_id(self, id: int) -> UserEntity | None:
        return self.get_by_id(id)

    def get_user_by_email(self, email: str) -> UserEntity | None:
        stmt = select(UserEntity).where(UserEntity.email == email)
        return self.db.execute(stmt).scalar_one_or_none()
