from shared.exceptions import AppException


class ProductException(AppException):
    pass


class ProductNotFound(ProductException):
    status_code = 404
    message = "The entered product was not found"


class ProductHasAlreadyStatus(ProductException):
    status_code = 409
    message = "The entered product already has the status"
