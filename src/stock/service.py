from shared.service import BaseService

from products.interfaces import IStockService
from .entity import StockEntity
from .repository import StockRepository
from products.repository import ProductRepository
from .exceptions import StockNotFound
from .model import (
    StockDetail, 
    CreateStockModel, 
    UpdateStockModel, 
    derive_stock_status
)

from products.entity import ProductEntity
from products.model import ProductModel
from products.exceptions import ProductNotFound

class StockService(IStockService, BaseService):

    def __init__(self, stock_repository: StockRepository, product_repository: ProductRepository):
        self.stock_repository = stock_repository
        self.product_repository = product_repository

    def _get_product_by_id_or_none(self, product_id: int) -> ProductEntity:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFound()
        return product
        
    def _get_stock_by_id_or_none(self, id: int) -> StockNotFound | StockEntity:
        stock = self.stock_repository.get_stock_by_id(id)
        if not stock:
            raise StockNotFound()
        return stock

    def _serialize_stock(self, stock_instance: StockEntity) -> dict:
        stock_dict = stock_instance.to_dict()
        stock_dict["status"] = derive_stock_status(stock_dict.get("quantity"))
        return StockDetail.model_validate(stock_dict).model_dump()

    def create_stock(self, data: dict, product_created_model_dump: dict) -> StockEntity:
        data['product_id'] = product_created_model_dump.get('id')
        stock_model_instance = CreateStockModel.model_validate(data).model_dump()

        stock_entity = StockEntity(**stock_model_instance)
        return self.stock_repository.create_stock(stock_entity)
    
    def update_stock(self, id: int, data: dict) -> StockEntity:
        stock = self._get_stock_by_id_or_none(id)
        stock_model_dump = UpdateStockModel.model_validate(data).model_dump(exclude_unset=True)

        stock_to_update = self._update_instance_entity(stock_model_dump, stock)
        return self.stock_repository.update_stock(stock_to_update)
    
    def get_stock_by_id(self, id: int) -> dict:
        stock_instance = self._get_stock_by_id_or_none(id)        
        product_instance = self._get_product_by_id_or_none(stock_instance.product_id)

        stock = self._serialize_stock(stock_instance)
        product = ProductModel.model_validate(product_instance.to_dict()).model_dump()
        return {"stock": stock, "product": product}

    def get_stock_low(self, page: int, per_page: int, company_id: int) -> tuple[list[dict], int]:
        stock_list = []
        registers, total = self.stock_repository.get_stock_low_quantity(page, per_page, company_id)
        for register in registers:
            stock = self._serialize_stock(register[0])
            product = ProductModel.model_validate(register[1].to_dict()).model_dump()
            stock_list.append({"stock": stock, "product": product})
        return stock_list, total

    def get_stock_detailed_with_product(self, page: int, per_page: int, company_id: int) -> tuple[list[dict], int]:
        stocks = []
        registers, total = self.stock_repository.get_stock_detailed(page, per_page, company_id)
        for register in registers:
            stock = self._serialize_stock(register[0])
            product = ProductModel.model_validate(register[1].to_dict()).model_dump()
            stocks.append({"stock": stock, "product": product})
        return stocks, total