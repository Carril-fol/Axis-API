from shared.exceptions import AppException


class PermissionException(AppException):
    pass


class PermissionNotFound(PermissionException):
    status_code = 404
    message = "Permission does not found."


class PermissionAlreadyExists(PermissionException):
    status_code = 409
    message = "Permission with that name already exists."
