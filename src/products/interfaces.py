from abc import ABC, abstractmethod

from .entity import ProductEntity


class IProductService(ABC):

    @abstractmethod
    def get_product_by_id(self, id: int) -> dict:
        pass

    @abstractmethod
    def get_products(self, company_id: int, page: int, per_page: int, search: str = None) -> list[dict]:
        pass

    @abstractmethod
    def create_product(self, data: dict, company_id: int) -> ProductEntity:
        pass

    @abstractmethod
    def update_product(self, id: int, data: dict) -> ProductEntity:
        pass

    @abstractmethod
    def deactivate_product(self, id: int, data: dict) -> ProductEntity:
        pass

    @abstractmethod
    def get_products_by_category_id(self, company_id: int, id: int) -> list[dict]:
        pass

    @abstractmethod
    def get_product_by_name(self, name: str, company_id: int) -> ProductEntity:
        pass
    
    @abstractmethod
    def reassign_category(self, company_id, product, id):
        pass
