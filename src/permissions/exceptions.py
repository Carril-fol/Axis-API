from shared.exceptions import AppException


class PermissionException(AppException):
    pass


class PermissionAlreadyExists(PermissionException):
    status_code = 409
    message = "Permission with that name already exists."
