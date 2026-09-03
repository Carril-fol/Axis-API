from shared.security import verify_password

from users.interfaces import IUserService

from .interfaces import IAuthService
from .model import LoginInput
from .exceptions import UserNotFound, InvalidCredentials


class AuthService(IAuthService):
    
    def __init__(self, user_service: IUserService):
        self.user_service = user_service

    def _verify_password(self, hashed: str, plain: str):
        if not verify_password(hashed, plain):
            raise InvalidCredentials()

    def authenticate(self, data: LoginInput) -> int:
        user = self.user_service.get_user_by_email(data.email)
        if not user:
            raise UserNotFound()

        self._verify_password(user.password, data.password)
        return user.id
