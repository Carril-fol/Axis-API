from shared.exceptions import AppException


class UserWithAnEmailAlreadyExists(AppException):
    status_code = 409
    message = "An user already exists with that email."


class UserCompanyNotFound(AppException):
    status_code = 404
    message = "User not found"


class UserCompanyInsufficientRolePrivileges(AppException):
    status_code = 403
    message = "You cannot do this action"
