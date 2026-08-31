from sqlalchemy import select, func

from shared.database.base_repository import BaseRepository
from .entity import StockEntity
from products.entity import ProductEntity


LOW_STOCK_THRESHOLD = 10


class StockRepository(BaseRepository):

    def __init__(self):
        super().__init__(StockEntity)

    def create_stock(self, stock: StockEntity) -> StockEntity:
        return self.create(stock)

    def update_stock(self, stock: StockEntity) -> StockEntity:
        return self.update(stock)

    def get_stock_by_id(self, id: int) -> StockEntity | None:
        return self.get_by_id(id)

    def get_stock_by_product_id(self, product_id: int) -> StockEntity | None:
        stmt = select(StockEntity).where(StockEntity.product_id == product_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_stock_low_quantity(self, page: int, per_page: int, company_id: int):
        return self._paginate_with_product(
            page,
            per_page,
            StockEntity.quantity < LOW_STOCK_THRESHOLD,
            ProductEntity.company_id == company_id,
            ProductEntity.status != "INACTIVE",
        )

    def get_stock_detailed(self, page: int, per_page: int, company_id: int):
        return self._paginate_with_product(
            page,
            per_page,
            ProductEntity.company_id == company_id,
            ProductEntity.status != "INACTIVE",
        )

    def _paginate_with_product(self, page: int, per_page: int, *filters):
        total = self.db.scalar(
            select(func.count())
            .select_from(StockEntity)
            .join(ProductEntity, StockEntity.product_id == ProductEntity.id)
            .where(*filters)
        )

        stmt = (
            select(StockEntity, ProductEntity)
            .join(ProductEntity, StockEntity.product_id == ProductEntity.id)
            .where(*filters)
            .order_by(StockEntity.id)
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        return self.db.execute(stmt).all(), total
