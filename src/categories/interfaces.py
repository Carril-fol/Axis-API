from abc import ABC, abstractmethod

from .entity import CategoryEntity
from .model import DetailCategoryModel, ListDetailCategoryModel


class ICategoryService(ABC):

    @abstractmethod
    def get_category_by_id(self, id: int, company_id: int) -> dict:
        pass

    @abstractmethod
    def create_category(self, data: dict, company_id: int) -> CategoryEntity:
        pass

    @abstractmethod
    def get_all_categories_from_company(self, company_id: int, page: int, per_page: int) -> ListDetailCategoryModel:
        pass

    @abstractmethod
    def update_category(self, id: int, data: dict, company_id: int) -> CategoryEntity:
        pass

    @abstractmethod
    def delete_category(self, id: int, data: dict, company_id: int) -> CategoryEntity:
        pass

    @abstractmethod
    def get_category_by_name(self, name: str, company_id: int) -> DetailCategoryModel:
        pass
