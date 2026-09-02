from abc import ABC, abstractmethod

from .entity import StockEntity


class IStockService(ABC):

    @abstractmethod
    def create_stock(self, data: dict, product_created_model_dump: dict) -> StockEntity:
        pass

    @abstractmethod
    def zero_quantity_for_product(self, product_id: int) -> None:
        pass

    @abstractmethod
    def update_stock(self, id: int, data: dict) -> StockEntity:
        pass

    @abstractmethod
    def get_stock_by_id(self, id: int) -> dict:
        pass

    @abstractmethod
    def get_stock_low(self, page: int, per_page: int, company_id: int) -> tuple[list[dict], int]:
        pass

    @abstractmethod
    def get_stock_detailed_with_product(self, page: int, per_page: int, company_id: int) -> tuple[list[dict], int]:
        pass
