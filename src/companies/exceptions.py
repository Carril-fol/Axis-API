from shared.exceptions import AppException


class CompanyException(AppException):
    pass


class CompanyNotFound(CompanyException):
    status_code = 404
    message = "Company does not found."


class CompanyInsufficientRolePrivileges(CompanyException):
    status_code = 403
    message = "You don't have privileges for this action."
