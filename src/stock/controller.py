import math
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from spectree import Response
from core.extensions import spectree
from shared.models import ErrorOutput, MessageResponse

from .middleware import require_stock_from_same_company
from .model import (
    UpdateStockInput,
    StockListDetail,
    StockItemResponse
)

from role_permissions.middleware import require_permission
from shared.authz import get_current_user_company


from container import stock_service

stock_blueprint = Blueprint(
    'stock_controller', 
    __name__, 
    url_prefix='/stock/api/v1'
)


@stock_blueprint.route('/get/all', methods=['GET'])
@jwt_required()
@require_permission("read_stock")
@spectree.validate(
    resp=Response(
        HTTP_200=StockListDetail,
        HTTP_400=ErrorOutput,
        HTTP_404=ErrorOutput,
        HTTP_500=ErrorOutput,
    ),
    tags=["Stock"]
)
def get_all_stock():
    user_data = get_current_user_company()
    company_id = user_data.company_id

    page: int = max(request.args.get('page', 1, type=int), 1)
    per_page: int = min(max(request.args.get('per_page', 10, type=int), 1), 100)

    stock_data, total = stock_service.get_stock_detailed_with_product(page, per_page, company_id)
    return {
        "data": stock_data,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": math.ceil(total / per_page) if total else 0
    }, 200


@stock_blueprint.route('/get/<int:id>', methods=['GET'])
@jwt_required()
@require_stock_from_same_company()
@require_permission("read_stock")
@spectree.validate(
    resp=Response(
        HTTP_200=StockItemResponse,
        HTTP_404=ErrorOutput,
        HTTP_500=ErrorOutput,
    ),
    tags=["Stock"]
)
def get_stock_by_id(id: int):
    stock = stock_service.get_stock_by_id(id)
    return {'data': stock}, 200


@stock_blueprint.route('/update/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@require_stock_from_same_company()
@require_permission("update_stock")
@spectree.validate(
    json=UpdateStockInput,
    resp=Response(
        HTTP_200=MessageResponse,
        HTTP_400=ErrorOutput,
        HTTP_404=ErrorOutput,
        HTTP_500=ErrorOutput,
    ),
    tags=["Stock"]
)
def update_stock(id: int, json: UpdateStockInput):
    data = json.model_dump(exclude_unset=True)

    stock_service.update_stock(id, data)
    return {'msg': 'Stock updated successfully'}, 200


@stock_blueprint.route('/get/low', methods=['GET'])
@jwt_required()
@require_permission("read_stock")
@spectree.validate(
    resp=Response(
        HTTP_200=StockListDetail,
        HTTP_400=ErrorOutput,
        HTTP_404=ErrorOutput,
        HTTP_500=ErrorOutput,
    ),
    tags=["Stock"]
)
def get_low_stock():
    user_data = get_current_user_company()
    company_id = user_data.company_id
    
    page: int = max(request.args.get('page', 1, type=int), 1)
    per_page: int = min(max(request.args.get('per_page', 10, type=int), 1), 100)

    data, total = stock_service.get_stock_low(page, per_page, company_id)
    return {
        'data': data,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total / per_page) if total else 0
    }, 200
