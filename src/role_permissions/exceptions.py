from shared.exceptions import AppException


class RolePermissionException(AppException):
    pass


class RolePermissionNotFound(RolePermissionException):
    status_code = 404
    message = "Not found Role Permission"


class RolePermissionsAlreadyHasAPermission(RolePermissionException):
    status_code = 409
    message = "The Role already has this permission"


class RoleNotInCompany(RolePermissionException):
    status_code = 403
    message = "Role does not belong to this company"
