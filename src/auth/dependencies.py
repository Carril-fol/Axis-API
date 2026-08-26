from users.user_orchestrator import user_service
from .auth_service import AuthService


auth_service = AuthService(user_service)