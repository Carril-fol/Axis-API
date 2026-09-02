from core.extensions import spectree, limiter
from shared.models import ErrorOutput, MessageResponse

from spectree import Response
from flask import Blueprint
from flask_jwt_extended import jwt_required

from .middleware import require_permission
from .model import (
    AssignRolePermissionInput,
    UpdateRolePermissionInput,
    DeleteRolePermissionQuery,
    ListRolePermissionsOutput
)
from shared.authz import get_current_user_company

from container import role_permission_service

role_permission_controller = Blueprint(
    "role-permission",
    __name__,
    url_prefix="/role-permissions/api/v1"
)


@role_permission_controller.route("/assign-permission-to-role", methods=["POST"])
@limiter.limit("5 per minute")
@jwt_required()
@require_permission("create_role_permission")
@spectree.validate(
    json=AssignRolePermissionInput,
    resp=Response(
        HTTP_201=MessageResponse,
        HTTP_400=ErrorOutput,
        HTTP_429=ErrorOutput,
    ),
    tags=["Role-permissions"]
)
def assign_role_permission(json: AssignRolePermissionInput):
    data = json.model_dump()
    user_data = get_current_user_company()
    company_id = user_data.company_id

    role_permission_service.assign_role_permission(data, company_id)
    return {"msg": "Role Permission assigned successfuly"}, 201


@role_permission_controller.route("/update/<int:id>", methods=["PUT", "PATCH"])
@limiter.limit("5 per minute")
@jwt_required()
@require_permission("update_role_permission")
@spectree.validate(
    json=UpdateRolePermissionInput,
    resp=Response(
        HTTP_200=MessageResponse,
        HTTP_403=ErrorOutput,
        HTTP_404=ErrorOutput,
    ),
    tags=["Role-permissions"]
)
def update_role_permission(id: int, json: UpdateRolePermissionInput):
    data = json.model_dump(exclude_unset=True)
    user_data = get_current_user_company()
    company_id = user_data.company_id

    role_permission_service.update_role_permission(id, data, company_id)
    return {"msg": "Role Permission updated successfully"}, 200


@role_permission_controller.route("/get/<int:role_id>", methods=["GET"])
@jwt_required()
@require_permission("read_role_permission")
@spectree.validate(
    resp=Response(
        HTTP_200=ListRolePermissionsOutput,
        HTTP_403=ErrorOutput,
    ),
    tags=["Role-permissions"]
)
def list_role_permissions(role_id: int):
    user_data = get_current_user_company()
    company_id = user_data.company_id
    
    permissions = role_permission_service.list_permissions_by_role_id(role_id, company_id)
    return {"role_id": role_id, "permissions": permissions}, 200


@role_permission_controller.route("/revoke", methods=["DELETE"])
@limiter.limit("5 per minute")
@jwt_required()
@require_permission("delete_role_permission")
@spectree.validate(
    query=DeleteRolePermissionQuery,
    resp=Response(
        HTTP_200=MessageResponse,
        HTTP_403=ErrorOutput,
        HTTP_404=ErrorOutput,
    ),
    tags=["Role-permissions"]
)
def revoke_role_permission(query: DeleteRolePermissionQuery):
    user_data = get_current_user_company()
    company_id = user_data.company_id

    role_permission_service.revoke_permission(query.role_id, query.permission_id, company_id)
    return {"msg": "Permission revoked successfully"}, 200
