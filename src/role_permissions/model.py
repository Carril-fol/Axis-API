from pydantic import BaseModel, Field


class CRUDRolePermissionModel(BaseModel):
    role_id: int = Field(..., description="ID of the role that receives the permissions", examples=[2])
    permission_id: list[int] = Field(..., description="IDs of the permissions to grant, in one call", examples=[[1, 2]])


class UpdateRolePermissionModel(BaseModel):
    role_id: int = Field(..., description="ID of the role the link points to", examples=[2])
    permission_id: int = Field(..., description="ID of the permission the link points to", examples=[3])


class UpdateRolePermissionInput(UpdateRolePermissionModel):
    pass    


class DeleteRolePermissionQuery(BaseModel):
    role_id: int = Field(..., description="ID of the role to revoke the permission from", examples=[2])
    permission_id: int = Field(..., description="ID of the permission to revoke", examples=[2])


class AssignRolePermissionModel(CRUDRolePermissionModel):
    pass


class AssignRolePermissionInput(CRUDRolePermissionModel):
    pass


class ListRolePermissionsOutput(BaseModel):
    role_id: int = Field(..., description="ID of the role", examples=[2])
    permissions: list[str] = Field(..., description="Permission names granted to the role", examples=[["CREATE_USER", "READ_USER"]])
