import math
from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from spectree import Response

from container import category_service
from core.extensions import spectree
from shared.models import ErrorOutput, MessageResponse
from shared.authz import get_current_user_company, require_permission

from .model import (
    CreateCategoryInput,
    UpdateCategoryInput,
    DetailCategoryResponse,
    ListDetailCategoryModel
)


category_controller = Blueprint(
    'category_controller',
    __name__,
    url_prefix='/categories/api/v1'
)


@category_controller.route('/create', methods=['POST'])
@jwt_required()
@require_permission("create_category")
@spectree.validate(
    json=CreateCategoryInput,
    resp=Response(
        HTTP_201=MessageResponse, 
        HTTP_400=ErrorOutput
    ),
    tags=["Categories"]
)
def create_category(json: CreateCategoryInput):
    user_company = get_current_user_company()
    company_id = user_company.company_id

    category_service.create_category(json, company_id)
    return {'msg': 'Category created successfully'}, 201


@category_controller.route('/get/<int:id>', methods=['GET'])
@jwt_required()
@require_permission("read_category")
@spectree.validate(
    resp=Response(
        HTTP_200=DetailCategoryResponse,
        HTTP_404=ErrorOutput
    ),
    tags=["Categories"]
)
def get_category_by_id(id: int):
    user_company = get_current_user_company()
    company_id = user_company.company_id

    category = category_service.get_category_by_id(id, company_id)

    return {'category': category}, 200


@category_controller.route('/get/all', methods=['GET'])
@jwt_required()
@require_permission("read_category")
@spectree.validate(
    resp=Response(
        HTTP_200=ListDetailCategoryModel,
        HTTP_400=ErrorOutput
    ),
    tags=["Categories"]
)
def get_all_categories_from_company():
    user_company = get_current_user_company()
    company_id = user_company.company_id

    page = max(request.args.get('page', 1, type=int), 1)
    per_page = min(max(request.args.get('per_page', 10, type=int), 1), 100)

    categories, total = category_service.get_all_categories_from_company(company_id, page, per_page)

    return {
        "categories": categories,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": math.ceil(total / per_page) if total else 0
    }, 200


@category_controller.route('/update/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@require_permission("update_category")
@spectree.validate(
    json=UpdateCategoryInput,
    resp=Response(
        HTTP_200=MessageResponse, 
        HTTP_400=ErrorOutput
    ),
    tags=["Categories"]
)
def update_category(json: UpdateCategoryInput, id: int):
    user_company = get_current_user_company()
    company_id = user_company.company_id

    category_service.update_category(id, json, company_id)

    return {'msg': 'Category updated successfully'}, 200


@category_controller.route('/disable/<int:id>', methods=['DELETE'])
@jwt_required()
@require_permission("delete_category")
@spectree.validate(
    resp=Response(
        HTTP_200=MessageResponse, 
        HTTP_400=ErrorOutput
    ),
    tags=["Categories"]
)
def delete_category(id: int):
    data = {"status": "INACTIVE"}
    user_company = get_current_user_company()
    company_id = user_company.company_id

    category_service.delete_category(id, data, company_id)

    return {'msg': 'Category deleted successfully'}, 200


@category_controller.route('/search/<string:name>', methods=['GET'])
@jwt_required()
@require_permission("read_category")
@spectree.validate(
    resp=Response(
        HTTP_200=DetailCategoryResponse,
        HTTP_404=ErrorOutput
    ),
    tags=["Categories"]
)
def get_category_by_name(name: str):
    user_company = get_current_user_company()
    company_id = user_company.company_id

    category = category_service.get_category_by_name(name, company_id)
    return {'category': category}, 200
