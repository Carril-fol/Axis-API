from shared.exceptions import AppException


class RoleException(AppException):
    pass


class RoleNotFound(RoleException):
    status_code = 404
    message = "Role not founded"


class RoleIsAlreadyInactive(RoleException):
    status_code = 409
    message = "Role is already inactive"


class RoleIsAlreadyActive(RoleException):
    status_code = 409
    message = "Role is already active"


class UserNotInCompany(RoleException):
    status_code = 403
    message = "User does not belong to this company"


class RoleNameReserved(RoleException):
    status_code = 409
    message = "Role name is reserved and cannot be used."
