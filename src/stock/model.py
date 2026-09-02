from datetime import datetime
from email.utils import parsedate_to_datetime
from enum import StrEnum
from products.model import ProductModel
from shared.models import PaginatedResponse
from pydantic import BaseModel, Field, field_validator


class StockStatus(StrEnum):
    IN_STOCK = 'IN STOCK'
    LOW_STOCK = 'LOW STOCK'
    OUT_OF_STOCK = 'OUT OF STOCK'

LOW_STOCK_THRESHOLD = 10


def derive_stock_status(quantity: int) -> StockStatus:
    if not quantity or quantity <= 0:
        return StockStatus.OUT_OF_STOCK
    if quantity < LOW_STOCK_THRESHOLD:
        return StockStatus.LOW_STOCK
    return StockStatus.IN_STOCK


class BaseStockModel(BaseModel):
    product_id: int = Field(..., description='FK of the product')
    quantity: int = Field(default=0, description='Quantity of the product in stock')
    date_updated: datetime = Field(
        default_factory=datetime.now,
        description='Date of the last stock update'
    )

    @field_validator('date_updated', mode='before')
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            return parsedate_to_datetime(value)
        return value

    @field_validator('quantity')
    @classmethod
    def quantity_must_be_non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError('Quantity must be zero or greater')
        return value


class CreateStockModel(BaseStockModel):
    quantity: int = Field(..., ge=0, description='Initial quantity in stock')


class UpdateStockInput(BaseModel):
    quantity: int = Field(..., ge=0, description='New quantity on hand. Cannot be negative', examples=[48])


class UpdateStockModel(BaseModel):
    product_id: int | None = Field(default=None, description='FK of the product')
    quantity: int | None = Field(default=None, description='Quantity of the product in stock')
    date_updated: datetime | None = Field(default=None, description='Date of the last stock update')

    @field_validator('date_updated', mode='before')
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            return parsedate_to_datetime(value)
        return value

    @field_validator('quantity')
    @classmethod
    def quantity_must_be_non_negative(cls, value: int) -> int:
        if value is not None and value < 0:
            raise ValueError('Quantity must be zero or greater')
        return value


class StockDetail(BaseStockModel):
    id: int = Field(..., description="ID of the stock row", examples=[1])
    status: StockStatus = Field(..., description='Stock status derived from quantity')


class StockWithProductDetail(BaseModel):
    stock: StockDetail = Field(..., description="Stock row: quantity and derived status")
    product: ProductModel = Field(..., description="The product the stock belongs to")


class StockItemResponse(BaseModel):
    data: StockWithProductDetail = Field(..., description="Stock of a single product")


class StockListDetail(PaginatedResponse):
    data: list[StockWithProductDetail] = Field(..., description="Stock rows for the requested page")
