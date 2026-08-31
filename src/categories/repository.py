from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import Sequence

from shared.database.base_repository import BaseRepository
from .entity import CategoryEntity

class CategoryRepository(BaseRepository):

    def __init__(self):
        super().__init__(CategoryEntity)

    def get_category_by_id(self, id: int, company_id: int) -> CategoryEntity | None:
        filters = [CategoryEntity.id == id, CategoryEntity.company_id == company_id]
        stmt = select(CategoryEntity).where(*filters)
        return self.db.execute(stmt).scalar_one_or_none()
     
    def get_categories_by_company_id(
        self,
        company_id: int,
        page: int = 1,
        per_page: int = 10,
        search: str = None
    ) -> tuple[Sequence[CategoryEntity], int | None]:
        filters = [CategoryEntity.company_id == company_id]
        
        if search:
            filters.append(CategoryEntity.name.ilike(f"%{search}%"))

        total_query = select(func.count()).select_from(CategoryEntity).where(*filters)
        total = self.db.scalar(total_query)

        stmt = (
            select(CategoryEntity)
            .where(*filters)
            .order_by(CategoryEntity.id)
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        categories = self.db.scalars(stmt).all()
        return categories, total
    
    def get_category_by_name(self, name: str, company_id: int) -> CategoryEntity | None:
        stmt = select(CategoryEntity).where(
            CategoryEntity.name == name,
            CategoryEntity.company_id == company_id
        )
        return self.db.execute(stmt).scalar_one_or_none()