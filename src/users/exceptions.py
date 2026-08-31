from shared.exceptions import AppException


class UserNotFound(AppException):
    status_code = 404
    message = "Invalid credentials."


class EmailInvalidFormat(AppException):
    status_code = 400
    message = "The email format is invalid."


class UserWithAnEmailAlreadyExists(AppException):
    status_code = 409
    message = "A User with that email already exists."


class PasswordDontMatch(AppException):
    status_code = 400
    message = "Invalid credentials."
