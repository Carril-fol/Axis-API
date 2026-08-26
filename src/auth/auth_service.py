from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from users.interfaces import IUserService

from .interfaces import IAuthService
from .auth_model import RegisterWithCompanyInput, LoginInput
from .exceptions import UserNotFound, InvalidCredentials


ph = PasswordHasher()


class AuthService(IAuthService):
    
    def __init__(self, user_service: IUserService):
        self.user_service = user_service

    def _verify_password(self, hashed: str, plain: str):
        try:
            ph.verify(hashed, plain)
        except VerifyMismatchError:
            raise InvalidCredentials()

    def register(self, data: RegisterWithCompanyInput) -> int:
        return self.user_service.register_owner(
            data.user.model_dump(),
            data.company.model_dump(),
        )  
    
    def authenticate(self, data: LoginInput) -> int:
        user = self.user_service.get_user_by_email(data.email)
        if not user:
            raise UserNotFound()

        self._verify_password(user.password, data.password)
        return user.id