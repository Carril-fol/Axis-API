from shared.service import BaseService

from products.interfaces import IProductService

from .entity import CategoryEntity
from .repository import CategoryRepository
from .interfaces import ICategoryService
from .exceptions import (
    CategoryNotFound, 
    CategoryStatusError, 
    CategoryNameReserved,
    CategoryAccessDeniedException
)
from .model import (
    CreateCategoryInput,
    UpdateCategoryInput,
    CreateCategoryModel,
    UpdateCategoryModel, 
    DetailCategoryModel, 
    ListDetailCategoryModel
)


RESERVED_CATEGORY_NAME = "OTHER"


class CategoryService(ICategoryService, BaseService):

    def __init__(
        self, 
        category_respository: CategoryRepository, 
        product_service: IProductService
    ):
        self._category_repository = category_respository
        self._product_service = product_service
        
    def _get_category_or_raise(self, category_id: int) -> CategoryEntity:
        category = self._category_repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFound()
        return category

    def _create_default_category(self, company_id: int) -> CategoryEntity:
        existing = self._category_repository.get_category_by_name(
            RESERVED_CATEGORY_NAME, company_id
        )
        if existing:
            return existing

        category_model_dump = CreateCategoryModel.model_validate(
            {"name": RESERVED_CATEGORY_NAME, "status": "ACTIVE", "company_id": company_id}
        ).model_dump()

        return self._category_repository.create(CategoryEntity(**category_model_dump))

    def _reassign_products_to_other(self, category_id: int, company_id: int) -> None:
        fallback = self._create_default_category(company_id)
        self._product_service.reassign_category(company_id, category_id, fallback.id)

    def get_category_by_id(self, id: int, company_id: int) -> dict:
        category = self._get_category_or_raise(id)
        if category.company_id != company_id:
            raise CategoryAccessDeniedException()
        
        return DetailCategoryModel.model_validate(category).model_dump()

    def create_category(self, data: CreateCategoryInput, company_id: int) -> CategoryEntity:
        if data.name.upper() == RESERVED_CATEGORY_NAME:
            raise CategoryNameReserved()

        category_model_dump = CreateCategoryModel.model_validate(
            {**data.model_dump(), "company_id": company_id}
        ).model_dump()

        category_entity = CategoryEntity(**category_model_dump)
        return self._category_repository.create(category_entity)
    
    def get_all_categories_from_company(self, company_id: int, page: int, per_page: int ) -> ListDetailCategoryModel:
        categories_raw, total = self._category_repository.get_categories_by_company_id(company_id, page, per_page)
        categories = [DetailCategoryModel.model_validate(category).model_dump() for category in categories_raw]
        return categories, total

    def update_category(self, id: int, data: UpdateCategoryInput, company_id: int) -> CategoryEntity:
        if data.name and data.name == RESERVED_CATEGORY_NAME:
            raise CategoryNameReserved()
        
        category: CategoryEntity = self._get_category_or_raise(id)
        
        if category.company_id != company_id:
            raise CategoryAccessDeniedException()
        
        category_model_dump = UpdateCategoryModel.model_validate(
            {**data.model_dump(exclude_unset=True), "company_id": category.company_id}
        ).model_dump(exclude_unset=True)
        
        category_entity = self._update_instance_entity(category_model_dump, category)
        return self._category_repository.update(category_entity)
    
    def delete_category(self, id: int, data: dict, company_id: int) -> CategoryEntity:
        category: CategoryEntity = self._get_category_or_raise(id)
        
        if category.company_id != company_id:
            raise CategoryAccessDeniedException()

        if category.status == data["status"]:
            raise CategoryStatusError()
        
        self._reassign_products_to_other(category.id, company_id)

        category_entity = self._update_instance_entity(data, category)
        return self._category_repository.update(category_entity)

    def get_category_by_name(self, name: str, company_id: int) -> DetailCategoryModel:    
        category = self._category_repository.get_category_by_name(name.upper(), company_id)
        if not category:
            raise CategoryNotFound()
        
        if category.company_id != company_id:
            raise CategoryAccessDeniedException()
        
        return DetailCategoryModel.model_validate(category).model_dump()
