from enum import StrEnum
from shared.models import PaginatedResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class RoleStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class BaseRoleModel(BaseModel):
    name: str = Field(..., description="The name of the role")
    status: RoleStatus = Field(default=RoleStatus.ACTIVE, description="Role status")
    company_id: int = Field(..., description="The ID of the associated company")

    @field_validator('name', mode='before')
    @classmethod
    def normalize_name(cls, value: str) -> str:
        if isinstance(value, str):
            return value.upper()
        return value


class CreateRoleModel(BaseRoleModel):
    pass


class CreateRoleInput(BaseModel):
    name: str = Field(..., description="The name of the role")

    @field_validator('name', mode='before')
    @classmethod
    def normalize_name(cls, value: str) -> str:
        if isinstance(value, str):
            return value.upper()
        return value


class UpdateRoleInput(BaseModel):
    name: str | None = Field(default=None, description="Updated role name")
    status: RoleStatus | None = Field(default=None, description="Updated role status")

    @field_validator('name', mode='before')
    @classmethod
    def normalize_name(cls, value: str) -> str:
        if isinstance(value, str):
            return value.upper()
        return value

    @model_validator(mode='after')
    def at_least_one_field(self) -> 'UpdateRoleInput':
        if self.name is None and self.status is None:
            raise ValueError('At least one field must be provided for update')
        return self


class DetailRoleModel(BaseRoleModel):
    id: int = Field(..., description="Role ID")

    model_config = ConfigDict(from_attributes=True)


class RoleListDetail(PaginatedResponse):
    data: list[DetailRoleModel] = Field(..., description="Roles of the company for the requested page")


class AssignRoleInput(BaseModel):
    user_id: int = Field(..., description="The ID of the user to assign the role to")
    role_id: int = Field(..., description="The ID of the role to assign")
