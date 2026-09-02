from shared.service import BaseService

from .entity import ProductEntity
from .repository import ProductRepository
from .exceptions import ProductNotFound, ProductHasAlreadyStatus
from .model import (
    ProductModel, 
    UpdateProductModel,
    DetailProductModel,
    CreateProductModel,
    CreateProductInputModel
)

from stock.interfaces import IStockService
from .interfaces import IProductService


class ProductService(IProductService, BaseService):

    def __init__(
            self, 
            product_repository: ProductRepository, 
            stock_service: IStockService
        ):
        self._product_repository = product_repository
        self._stock_service = stock_service
    
    def _product_exist_by_id(self, id: int) -> ProductNotFound | ProductEntity:
        product = self._product_repository.get_by_id(id)
        if not product:
            raise ProductNotFound()
        return product
    
    def _validate_status_change(self, product: ProductEntity, data: dict) -> ProductHasAlreadyStatus | ProductEntity:
        status = data.get("status") 
        if status is not None and status == product.status:
            raise ProductHasAlreadyStatus()
        return product

    def get_product_by_id(self, id: int) -> dict:
        product = self._product_exist_by_id(id)
        return DetailProductModel.model_validate(product).model_dump()
    
    def get_products(self, company_id: int, page: int, per_page: int, search: str = None) -> list[dict]:
        products_db, total = self._product_repository.get_products(company_id, page, per_page, search)
        products = [ProductModel.model_validate(product).model_dump() for product in products_db]
        return products, total

    def get_products_by_category_id(self, company_id: int, id: int) -> list[dict]:
        products_raw = self._product_repository.get_products_by_category_id(company_id, id)
        return [ProductModel.model_validate(product).model_dump() for product in products_raw]
    
    def get_product_by_name(self, name: str, company_id: int) -> ProductEntity:
        name = str.upper(name)
        product = self._product_repository.get_product_by_name(name, company_id)
        
        if not product:
            raise ProductNotFound()

        return ProductModel.model_validate(product).model_dump()

    def create_product(self, data: CreateProductInputModel, company_id: int) -> ProductEntity:
        product_data_validated = CreateProductModel.model_validate(
            {**data, "company_id": company_id}
        ).model_dump()
        product_entity = ProductEntity(**product_data_validated)

        product_created = self._product_repository.create(product_entity)
        product_created_model_dump = ProductModel.model_validate(product_created).model_dump()
        
        self._stock_service.create_stock(data, product_created_model_dump)
        return product_created

    def update_product(self, id: int, data: dict) -> ProductEntity:
        product = self._product_exist_by_id(id)
        self._validate_status_change(product, data)
        
        product_model_validated_data = UpdateProductModel.model_validate(data).model_dump(exclude_unset=True)
        product_to_update = self._update_instance_entity(product_model_validated_data, product)
        return self._product_repository.update(product_to_update)

    def deactivate_product(self, id: int, data: dict) -> ProductEntity:
        product = self._product_exist_by_id(id)
        self._validate_status_change(product, data)

        product_to_deactivate = self._update_instance_entity(data, product)
        product_deactivated = self._product_repository.update(product_to_deactivate)

        self._stock_service.zero_quantity_for_product(id)
        return product_deactivated

    def reassign_category(self, company_id: int, from_category_id: int, to_category_id: int) -> int:
        return self._product_repository.reassign_category(company_id, from_category_id, to_category_id)
