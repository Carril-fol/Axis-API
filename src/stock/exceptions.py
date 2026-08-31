from shared.exceptions import AppException


class StockException(AppException):
    pass


class StockNotFound(StockException):
    status_code = 404
    message = "Stock not found."
