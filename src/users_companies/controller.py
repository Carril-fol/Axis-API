from spectree import Response
from flask import Blueprint
from flask_jwt_extended import jwt_required

from core.extensions import spectree, limiter
from shared.authz import get_current_user_company
from .model import RegisterInputFromCompany, UsersFromCompanyOutput

from container import user_company_service
from users.middleware import require_user_from_same_company
from users.model import (
    RegisterOutput,
    UpdateUserInput,
    UpdateUserOutput,
    DeleteUserOutput,
    ErrorOutput
)

from role_permissions.middleware import require_permission

users_companies_blueprint = Blueprint(
    "users_companies",
    __name__,
    url_prefix="/users/api/v1"
)


@users_companies_blueprint.route("/create-user-from-company", methods=["POST"])
@jwt_required()
@require_permission("create_user")
@spectree.validate(
    json=RegisterInputFromCompany,
    resp=Response(
        HTTP_201=RegisterOutput,
        HTTP_400=ErrorOutput,
        HTTP_422=ErrorOutput,
        HTTP_403=ErrorOutput
    ),
    tags=["users"]
)
def create_user_for_company(json: RegisterInputFromCompany):
    company_id: int = get_current_user_company().company_id

    user_company_service.create_user_for_company(json, company_id)
    return {"msg": "User created successfully"}, 201


@users_companies_blueprint.route("/update-user-from-company/<int:id>", methods=["PUT", "PATCH"])
@limiter.limit("3 per minute")
@jwt_required()
@require_user_from_same_company()
@require_permission("update_user")
@spectree.validate(
    json=UpdateUserInput,
    resp=Response(
        HTTP_200=UpdateUserOutput,
        HTTP_400=ErrorOutput,
        HTTP_422=ErrorOutput,
        HTTP_403=ErrorOutput
    ),
    tags=["users"]
)
def update_user_from_company(json: UpdateUserInput, id: int):
    data: dict = json.model_dump(exclude_unset=True)
    requesting_user_id: int = get_current_user_company().user_id

    user_company_service.update_user_from_company(id, data, requesting_user_id)
    return {"msg": "User updated successfully"}, 200


@users_companies_blueprint.route("/delete-user-from-company/<int:id>", methods=["DELETE"])
@limiter.limit("5 per hour")
@jwt_required()
@require_user_from_same_company()
@require_permission("delete_user")
@spectree.validate(
    resp=Response(
        HTTP_200=DeleteUserOutput,
        HTTP_400=ErrorOutput,
        HTTP_422=ErrorOutput,
        HTTP_403=ErrorOutput
    ),
    tags=["users"]
)
def delete_user_from_company(id: int):
    requesting_user_id: int = get_current_user_company().user_id

    user_company_service.delete_user_from_company(id, requesting_user_id)
    return {"msg": "User deleted successfully"}, 200


@users_companies_blueprint.route("/get-users-from-company", methods=["GET"])
@limiter.limit("5 per hour")
@jwt_required()
@require_permission("read_user")
@spectree.validate(
    resp=Response(
        HTTP_200=UsersFromCompanyOutput,
        HTTP_403=ErrorOutput
    ),
    tags=["users"]
)
def get_users_from_company():
    company_id: int = get_current_user_company().company_id
    users = user_company_service.get_users_from_company(company_id)
    return {"users": users}, 200
