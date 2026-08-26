from abc import ABC, abstractmethod

from .auth_model import RegisterWithCompanyInput, LoginInput


class IAuthService(ABC):
    
    @abstractmethod
    def register(self, data: RegisterWithCompanyInput):
        pass
    
    @abstractmethod
    def authenticate(self, data: LoginInput):
        pass