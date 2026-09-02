from datetime import datetime
from email.utils import parsedate_to_datetime
from enum import StrEnum
from shared.models import PaginatedResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def _upper(value: str) -> str:
    return value.upper()

def _must_contain_letters(value: str) -> str:
    if not any(char.isalpha() for char in value):
        raise ValueError("Name must contain alphabet characters.")
    return value



class ProductStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class BaseProductModel(BaseModel):
    name: str = Field(..., min_length=3, max_length=180, description="Name of the product")
    description: str = Field(..., min_length=0, max_length=500, description="Description of the product")
    category_id: int = Field(..., description="Id from the category")
    company_id: int = Field(..., description="Id from the company")
    status: ProductStatus = Field(default=ProductStatus.ACTIVE, description="Status of the product, defaults to 'ACTIVE'")
    date_creation: datetime = Field(default_factory=datetime.now, description="Date of the creation product")
    date_updated: datetime = Field(default_factory=datetime.now, description="Date of the last update from the product")

    @field_validator("*", mode="before")
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @field_validator("date_creation", "date_updated", mode="before")
    @classmethod
    def parse_data(cls, value):
        if isinstance(value, str):
            return parsedate_to_datetime(value)
        return value

    @field_validator("name")
    @classmethod
    def name_must_contain_alphabet_characters(cls, value):
        if not any(str(c).isalpha() for c in value):
            raise ValueError("Name must contain alphabet characters.")
        return value

    @field_validator("category_id")
    @classmethod
    def category_id_must_be_greater_than_0(cls, value):
        if value <= 0:
            raise ValueError("Category ID must be greater than 0.")
        return value


class CreateProductModel(BaseProductModel):
    description: str = Field(..., min_length=1, max_length=500)


class ProductModel(BaseProductModel):
    id: int = Field(..., description="ID of the product")
    model_config = ConfigDict(from_attributes=True)


class DetailProductModel(ProductModel):
    pass


class DetailProductResponse(BaseModel):
    product: DetailProductModel = Field(..., description="Product detail wrapped in the response envelope")


class ListDetailProductModel(PaginatedResponse):
    products: list[DetailProductModel] = Field(..., description="List of products with detailed information")


class UpdateProductModel(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=180, description="Name of the product")
    description: str | None = Field(default=None, min_length=0, max_length=500, description="Description of the product")
    category_id: int | None = Field(default=None, description="Id from the category")
    company_id: int | None = Field(default=None, description="Id from the company")
    status: ProductStatus | None = Field(default=None, description="Status of the product")
    date_creation: datetime | None = Field(default=None, description="Date of the creation product")
    date_updated: datetime | None = Field(default=None, description="Date of the last update from the product")

    @field_validator("*", mode="before")
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @field_validator("date_creation", "date_updated", mode="before")
    @classmethod
    def parse_data(cls, value):
        if isinstance(value, str):
            return parsedate_to_datetime(value)
        return value

    @field_validator("name")
    @classmethod
    def name_must_contain_alphabet_characters(cls, value):
        if value and not any(str(c).isalpha() for c in value):
            raise ValueError("Name must contain alphabet characters.")
        return value

    @field_validator("category_id")
    @classmethod
    def category_id_must_be_greater_than_0(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Category ID must be greater than 0.")
        return value


class UpdateProductInputModel(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=180, description="Name of the product")
    description: str | None = Field(default=None, min_length=0, max_length=500, description="Description of the product")
    category_id: int | None = Field(default=None, description="Id from the category")
    status: ProductStatus | None = Field(default=None, description="Status of the product")
    date_updated: datetime | None = Field(default=None, description="Date of the last update from the product")

    @field_validator("*", mode="before")
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @model_validator(mode="after")
    def set_date_updated(self):
        self.date_updated = datetime.now()
        return self


class CreateProductInputModel(BaseModel):
    name: str = Field(..., min_length=3, max_length=180, description="Name of the product")
    description: str = Field(..., min_length=1, max_length=500, description="Description of the product")
    category_id: int = Field(..., description="Id from the category")
    quantity: int = Field(default=0, description="Quantity of the product")

    @field_validator("*", mode="before")
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
