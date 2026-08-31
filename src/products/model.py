from datetime import datetime
from email.utils import parsedate_to_datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Optional, Literal


class BaseProductModel(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=180, description="Name of the product")
    description: Optional[str] = Field(default=None, min_length=0, max_length=500, description="Description of the product")
    category_id: Optional[int] = Field(default=None, description="Id from the category")
    company_id: Optional[int] = Field(default=None, description="Id from the company")
    status: Optional[Literal["ACTIVE", "INACTIVE"]] = Field(default="ACTIVE", description="Status of the product, defaults to 'ACTIVE'")
    date_creation: Optional[datetime] = Field(default_factory=datetime.now, description="Date of the creation product")
    date_updated: Optional[datetime] = Field(default_factory=datetime.now, description="Date of the last update from the product")

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


class CreateProductModel(BaseProductModel):
    name: str = Field(..., min_length=3, max_length=180)
    description: str = Field(..., min_length=1, max_length=500)
    category_id: int = Field(...)
    company_id: int = Field(...)


class ProductModel(BaseProductModel):
    id: Optional[int] = Field(default=None, description="ID of the product")
    model_config: ConfigDict = ConfigDict(from_attributes=True)


class DetailProductModel(BaseProductModel):
    id: Optional[int] = Field(default=None, description="ID of the product")


class ListDetailProductModel(BaseModel):
    products: list[DetailProductModel] = Field(..., description="List of products with detailed information")
    total: int = Field(..., description="Total number of products")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Number of products per page")
    total_pages: int = Field(..., description="Total number of pages")


class UpdateProductInputModel(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=180, description="Name of the product")
    description: Optional[str] = Field(default=None, min_length=0, max_length=500, description="Description of the product")
    category_id: Optional[int] = Field(default=None, description="Id from the category")
    status: Optional[Literal["ACTIVE", "INACTIVE"]] = Field(default=None, description="Status of the product")

    @field_validator("*", mode="before")
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @model_validator(mode="after")
    def set_date_updated(self):
        self.date_updated = datetime.now()
        return self

    date_updated: Optional[datetime] = Field(default=None, description="Date of the last update from the product")


class UpdateProductOutputModel(BaseModel):
    msg: str = Field(..., description="Message indicating the result of the product update", examples=["Product updated successfully"])


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


class CreateProductOutputModel(BaseModel):
    msg: str = Field(..., description="Message indicating the result of the product creation", examples=["Product created successfully"])


class DeleteProductModel(BaseModel):
    msg: str = Field(..., description="Message indicating the result of the product deletion", examples=["Product deleted successfully"])


class ErrorOutput(BaseModel):
    error: str