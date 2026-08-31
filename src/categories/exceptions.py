from shared.exceptions import AppException


class CategoryException(AppException):
    pass


class CategoryNotFound(CategoryException):
    status_code = 404
    message = "Category does not exist."


class CategoryAlreadyExists(CategoryException):
    status_code = 409
    message = "Category already exists."


class CategoryStatusError(CategoryException):
    status_code = 409
    message = "Category already has this status."


class CategoryNameReserved(CategoryException):
    status_code = 409
    message = "Category name is reserved and cannot be used."


class CategoryAccessDeniedException(CategoryException):
    status_code = 403
    message = "Cannot access this category"