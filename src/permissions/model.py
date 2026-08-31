from pydantic import BaseModel, ConfigDict, field_validator, Field

class CRUDPermissionBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)

    @field_validator("*", mode="before")
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value


class PermissionModel(CRUDPermissionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UpdatePermissionModel(CRUDPermissionBase):
    pass


class CreatePermissionModel(CRUDPermissionBase):
    pass

