from pydantic import BaseModel, Field


class CRUDRolePermissionModel(BaseModel):
    role_id: int
    permission_id: list[int]


class DetailRolePermissionModel(CRUDRolePermissionModel):
    id: int


class UpdateRolePermissionModel(BaseModel):
    role_id: int
    permission_id: int


class UpdateRolePermissionInput(UpdateRolePermissionModel):
    pass    


class UpdateRolePermissionOutput(BaseModel):
    msg: str = Field(..., examples=["Update successfuly"])


class DeleteRolePermissionQuery(BaseModel):
    role_id: int
    permission_id: int


class CreateRolePermissionModel(CRUDRolePermissionModel):
    pass


class CreateRolePermissionInput(CRUDRolePermissionModel):
    pass


class CreateRolePermissionOutput(BaseModel):
    msg: str = Field(..., examples=["Creation successfuly"])


class AssignRolePermissionModel(CRUDRolePermissionModel):
    pass


class AssignRolePermissionInput(CRUDRolePermissionModel):
    pass


class AssignRolePermissionOutput(BaseModel):
    msg: str = Field(..., examples=["Assignment successfuly"])


class ListRolePermissionsOutput(BaseModel):
    role_id: int = Field(..., description="The ID of the role")
    permissions: list[str] = Field(..., description="Permission names granted to the role")


class RevokeRolePermissionOutput(BaseModel):
    msg: str = Field(..., examples=["Permission revoked successfully"])


class ErrorOutput(BaseModel):
    error: str