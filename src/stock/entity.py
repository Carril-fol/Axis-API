from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from shared.database.database import Base
from products.entity import ProductEntity


class StockEntity(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, unique=True)
    quantity = Column(Integer, nullable=False)
    date_updated = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    products = relationship(ProductEntity)

    __table_args__ = (
        CheckConstraint('quantity >= 0', name='ck_stock_quantity_non_negative'),
    )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
