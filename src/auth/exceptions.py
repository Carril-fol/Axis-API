from shared.exceptions import AppException


class EmailInvalidFormat(AppException):
    status_code = 400
    message = "The email format is invalid."


class PasswordDontMatch(AppException):
    status_code = 400
    message = "Passwords do not match."


class InvalidCredentials(AppException):
    status_code = 401
    message = "Invalid credentials."


class UserNotFound(AppException):
    status_code = 401
    message = "Invalid credentials."
