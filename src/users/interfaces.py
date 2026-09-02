from abc import ABC, abstractmethod

from .entity import UserEntity


class IUserService(ABC):
    
    @abstractmethod
    def get_user_by_email(self, email: str) -> UserEntity | None:
        pass
    
    @abstractmethod
    def get_user_by_id(self, id: int) -> dict:
        pass

    @abstractmethod
    def update_user(self, id: int, data: dict):
        pass
    
    @abstractmethod
    def delete_user(self, id: int):
        pass
    
    @abstractmethod
    def create_user(self, data: dict) -> UserEntity:
        pass
