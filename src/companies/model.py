from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class BaseCompanyModel(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255, description="Name of the company")
    address: str | None = Field(default=None, min_length=5, max_length=255, description="Address of the company")
    country: str | None = Field(default=None, min_length=2, max_length=100, description="Country of the company")
    date_creation: datetime | None = Field(default=None, description="Date of the creation company")

    @field_validator("name", "address", "country", mode="before")
    @classmethod
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value


class CreateCompanyInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, description="Name of the company")
    country: str = Field(..., min_length=2, max_length=100, description="Country of the company")
    address: str = Field(..., min_length=5, max_length=255, description="Address of the company")


class CreateCompanyModel(BaseCompanyModel):
    name: str = Field(..., min_length=2, max_length=255)
    country: str = Field(..., min_length=2, max_length=100)
    address: str = Field(..., min_length=5, max_length=255)
    date_creation: datetime = Field(default_factory=datetime.now)


class UpdateCompanyInput(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255, description="Name of the company")
    address: str | None = Field(default=None, min_length=5, max_length=255, description="Address of the company")
    country: str | None = Field(default=None, min_length=2, max_length=100, description="Country of the company")


class DetailCompanyModel(BaseCompanyModel):
    id: int = Field(..., description="Id from company")
    model_config = ConfigDict(from_attributes=True)


class DetailCompanyResponse(BaseModel):
    company: DetailCompanyModel = Field(..., description="The company the current user belongs to")
