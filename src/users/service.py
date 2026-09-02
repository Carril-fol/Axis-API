from shared.service import BaseService

from .entity import UserEntity
from .repository import UserRepository
from .model import (
    CreateUserModel,
    DetailUserModel,
    UpdateUserModel,
)
from .exceptions import UserNotFound

from .interfaces import IUserService


class UserService(IUserService, BaseService):

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _get_user_or_raise(self, user_id: int) -> UserEntity:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound()
        return user

    def _format_user(self, user_entity: UserEntity) -> dict:
        return DetailUserModel.model_validate(
            user_entity.to_dict()
        ).model_dump()

    def create_user(self, data: dict) -> UserEntity:
        user_dump = CreateUserModel.model_validate(data).model_dump()
        return self.user_repository.create(UserEntity(**user_dump))

    def update_user(self, user_id: int, user_data: dict) -> UserEntity:
        user = self._get_user_or_raise(user_id)

        user_update_model_data = UpdateUserModel.model_validate(
            user_data
        ).model_dump(exclude_unset=True)

        user_to_update = self._update_instance_entity(user_update_model_data, user)
        return self.user_repository.update(user_to_update)

    def delete_user(self, user_id: int) -> None:
        user = self._get_user_or_raise(user_id)
        return self.user_repository.delete(user)

    def get_user_by_email(self, email: str) -> UserEntity | None:
        return self.user_repository.get_user_by_email(email)

    def get_user_by_id(self, user_id: int) -> dict:
        user = self._get_user_or_raise(user_id)
        return self._format_user(user)
