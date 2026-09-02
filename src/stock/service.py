from shared.service import BaseService

from .entity import StockEntity
from .repository import StockRepository
from .interfaces import IStockService
from .exceptions import StockNotFound
from .model import (
    StockDetail, 
    CreateStockModel, 
    UpdateStockModel, 
    derive_stock_status
)

from products.model import ProductModel


class StockService(IStockService, BaseService):

    def __init__(self, stock_repository: StockRepository):
        self.stock_repository = stock_repository

    def _get_stock_by_id_or_none(self, id: int) -> StockNotFound | StockEntity:
        stock = self.stock_repository.get_by_id(id)
        if not stock:
            raise StockNotFound()
        return stock

    def _serialize_stock(self, stock_instance: StockEntity) -> dict:
        stock_dict = stock_instance.to_dict()
        stock_dict["status"] = derive_stock_status(stock_dict.get("quantity"))
        return StockDetail.model_validate(stock_dict).model_dump()

    def _serialize_stock_with_product(self, stock_instance: StockEntity, product_instance) -> dict:
        return {
            "stock": self._serialize_stock(stock_instance),
            "product": ProductModel.model_validate(product_instance.to_dict()).model_dump()
        }

    def create_stock(self, data: dict, product_created_model_dump: dict) -> StockEntity:
        stock_data = {**data, "product_id": product_created_model_dump.get("id")}
        stock_model = CreateStockModel.model_validate(stock_data).model_dump()
        stock_entity = StockEntity(**stock_model)
        return self.stock_repository.create(stock_entity)

    def zero_quantity_for_product(self, product_id: int) -> None:
        stock = self.stock_repository.get_stock_by_product_id(product_id)
        if stock and stock.quantity != 0:
            stock.quantity = 0
            self.stock_repository.update(stock)

    def update_stock(self, id: int, data: dict) -> StockEntity:
        stock = self._get_stock_by_id_or_none(id)
        stock_model_dump = UpdateStockModel.model_validate(data).model_dump(exclude_unset=True)

        stock_to_update = self._update_instance_entity(stock_model_dump, stock)
        return self.stock_repository.update(stock_to_update)

    def get_stock_by_id(self, id: int) -> dict:
        register = self.stock_repository.get_stock_with_product(id)
        if not register:
            raise StockNotFound()
        return self._serialize_stock_with_product(register[0], register[1])

    def get_stock_low(self, page: int, per_page: int, company_id: int) -> tuple[list[dict], int]:
        registers, total = self.stock_repository.get_stock_low_quantity(page, per_page, company_id)
        return [self._serialize_stock_with_product(r[0], r[1]) for r in registers], total

    def get_stock_detailed_with_product(self, page: int, per_page: int, company_id: int) -> tuple[list[dict], int]:
        registers, total = self.stock_repository.get_stock_detailed(page, per_page, company_id)
        return [self._serialize_stock_with_product(r[0], r[1]) for r in registers], total
