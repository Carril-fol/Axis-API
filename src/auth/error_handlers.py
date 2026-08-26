from flask import Flask
from .exceptions import (
    UserNotFound, 
    InvalidCredentials, 
    PasswordDontMatch,
    EmailInvalidFormat
)

def register_auth_error_handlers(app: Flask) -> None:
    
    @app.errorhandler(UserNotFound)
    def handle_user_not_found(error):
        return {"error": "Invalid credentials."}, 401

    @app.errorhandler(PasswordDontMatch)
    def handle_password_dont_match(error):
        return {"error": str(error)}, 400
    
    @app.errorhandler(InvalidCredentials)
    def handle_invalid_credentials(error):
        return {"error": str(error)}, 401

    @app.errorhandler(EmailInvalidFormat)
    def handle_invalid_email(error):
        return {"error": str(error)}, 400