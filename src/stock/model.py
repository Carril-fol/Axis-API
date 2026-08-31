from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator

StatusType = Literal['IN STOCK', 'LOW STOCK', 'OUT OF STOCK']

LOW_STOCK_THRESHOLD = 10


def derive_stock_status(quantity: int) -> StatusType:
    """Stock status is derived from quantity, never persisted.

    The product lifecycle (ACTIVE/INACTIVE) lives on the product; here we only
    describe how much there is. A deactivated product cascades to quantity 0,
    which naturally reads as 'OUT OF STOCK'.
    """
    if not quantity or quantity <= 0:
        return 'OUT OF STOCK'
    if quantity < LOW_STOCK_THRESHOLD:
        return 'LOW STOCK'
    return 'IN STOCK'


class BaseStockModel(BaseModel):
    product_id: Optional[int] = Field(default=None, description='FK of the product')
    quantity: Optional[int] = Field(default=0, description='Quantity of the product in stock')
    date_updated: Optional[datetime] = Field(
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
        if value is not None and value < 0:
            raise ValueError('Quantity must be zero or greater')
        return value


class CreateStockModel(BaseStockModel):
    product_id: int = Field(..., description='FK of the product (required)')
    quantity: int = Field(..., ge=0, description='Initial quantity in stock')


class CreateStockInput(BaseModel):
    product_id: int = Field(..., description='FK of the product')
    quantity: int = Field(..., ge=0, description='Initial quantity in stock')


class CreateStockOutput(BaseModel):
    msg: str = Field(..., examples=["Create successful"])


class UpdateStockInput(BaseModel):
    quantity: int = Field(..., ge=0, description='Updated quantity')


class UpdateStockModel(BaseStockModel):
    pass


class UpdateStockOutput(BaseModel):
    msg: str = Field(..., examples=["Update successful"])


class StockDetail(BaseStockModel):
    id: int
    status: StatusType = Field(..., description='Stock status derived from quantity')


class StockWithProductDetail(BaseModel):
    stock: StockDetail
    product: dict


class StockItemResponse(BaseModel):
    data: StockWithProductDetail


class StockListDetail(BaseModel):
    data: list[StockWithProductDetail]
    total: int
    page: int
    per_page: int
    total_pages: int


class StockProductDetail(BaseModel):
    id: int = Field(..., description='Stock ID')
    product_id: int = Field(..., description='Product ID')
    quantity: int = Field(..., description='Current quantity of the product')
    status: StatusType = Field(..., description='Current stock status')
    name: str = Field(..., description='Product name')
    description: str = Field(..., description='Product description')
    category_id: int = Field(..., description='Product category ID')
    date_updated: datetime = Field(..., description='Last stock update date')
    date_creation: datetime = Field(..., description='Stock creation date')


class ErrorOutput(BaseModel):
    msg: str
