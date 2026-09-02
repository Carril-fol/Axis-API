from pydantic import BaseModel, ConfigDict, Field


class CRUDPermissionBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)


class PermissionModel(CRUDPermissionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CreatePermissionModel(CRUDPermissionBase):
    pass
