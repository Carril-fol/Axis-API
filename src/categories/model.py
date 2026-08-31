from enum import StrEnum
from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=150, description="Name of the category")

    status: CategoryStatus = Field(default=CategoryStatus.ACTIVE, description="Status of the category")

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value):
        if isinstance(value, str):
            value = value.strip().upper()

        return value

    @field_validator("name")
    @classmethod
    def name_must_contain_letters(cls, value):
        if not any(character.isalpha() for character in value):
            raise ValueError(
                "Name must contain at least one alphabetic character"
            )

        return value


class CategoryModel(CategoryBase):
    id: int | None = Field(default=None, description="ID of the category")
    company_id: int


class CreateCategoryInput(CategoryBase):
    pass


class CreateCategoryModel(CategoryBase):
    company_id: int


class UpdateCategoryInput(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=150)
    status: CategoryStatus | None = None

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value):
        if isinstance(value, str):
            return value.strip().upper()
        return value

    @field_validator("name")
    @classmethod
    def name_must_contain_letters(cls, value):
        if value is not None and not any(character.isalpha() for character in value):
            raise ValueError("Name must contain at least one alphabetic character")
        return value


class UpdateCategoryModel(UpdateCategoryInput):
    company_id: int


class DetailCategoryModel(CategoryModel):
    model_config = ConfigDict(from_attributes=True)


class DetailCategoryResponse(BaseModel):
    category: DetailCategoryModel = Field(..., description='Category detail wrapped in the response envelope')


class ListDetailCategoryModel(BaseModel):
    categories: list[DetailCategoryModel] = Field(..., description='List of categories with detailed information')
    total: int = Field(..., description='Total number of categories')
    page: int = Field(..., description='Current page number')
    per_page: int = Field(..., description='Number of categories per page')
    total_pages: int = Field(..., description='Total number of pages')


class CategoryOutputResponse(BaseModel):
    msg: str = Field(..., description='Error message')
    

class ErrorOutput(BaseModel):
    msg: str = Field(..., description='Error message')