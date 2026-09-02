from sqlalchemy import update, select, func
from sqlalchemy.orm import Session

from shared.database.base_repository import BaseRepository
from .entity import ProductEntity


class ProductRepository(BaseRepository):

    def __init__(self):
        super().__init__(ProductEntity)
        
    def get_products(
        self,
        company_id: int,
        page: int = 1,
        per_page: int = 10,
        search: str = None
    ) -> tuple[list[ProductEntity], int]:
        filters = [ProductEntity.company_id == company_id]

        if search:
            filters.append(ProductEntity.name.ilike(f"%{search}%"))

        total = self.db.scalar(
            select(func.count()).select_from(ProductEntity).where(*filters)
        )

        stmt = (
            select(ProductEntity)
            .where(*filters)
            .order_by(ProductEntity.id)
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        products = self.db.scalars(stmt).all()

        return list(products), total
    
    def get_products_by_category_id(self, company_id: int, id: int):
        stmt = select(ProductEntity).where(
            ProductEntity.category_id == id,
            ProductEntity.company_id == company_id
        )
        result = self.db.execute(stmt).scalars()
        return result

    def get_product_by_name(self, name: str, company_id: int):
        stmt = select(ProductEntity).where(
            ProductEntity.name == name, 
            ProductEntity.company_id == company_id  
        )
        return self.db.scalars(stmt).first()
        
    def reassign_category(self, company_id: int, from_category_id: int, to_category_id: int) -> int:
        stmt = (
            update(ProductEntity)
            .where(
                ProductEntity.company_id == company_id,
                ProductEntity.category_id == from_category_id,
            )
            .values(category_id=to_category_id)
        )
        result = self.db.execute(stmt)
        return result.rowcount
