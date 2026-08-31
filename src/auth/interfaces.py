from abc import ABC, abstractmethod

from .model import LoginInput


class IAuthService(ABC):

    @abstractmethod
    def authenticate(self, data: LoginInput):
        pass
