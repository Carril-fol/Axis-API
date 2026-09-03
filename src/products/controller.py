import math
from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from spectree import Response

from core.extensions import spectree
from shared.models import ErrorOutput, MessageResponse

from .model import (
    CreateProductInputModel,
    UpdateProductInputModel,
    DetailProductResponse,
    ListDetailProductModel
)

from shared.authz import (
    get_current_user_company,
    require_permission,
    require_product_from_same_company,
)


from container import product_service
product_controller = Blueprint(
    "product_controller",
    __name__,
    url_prefix="/products/api/v1"
)


@product_controller.route("/create", methods=["POST"])
@jwt_required()
@require_permission("create_product")
@spectree.validate(
    json=CreateProductInputModel,
    resp=Response(
        HTTP_201=MessageResponse,
        HTTP_400=ErrorOutput
    ),
    tags=["Product"]
)
def create_product(json: CreateProductInputModel):
    data = json.model_dump()
    user_company = get_current_user_company()
    company_id = user_company.company_id

    product_service.create_product(data, company_id)
    return {"msg": "Product created successfully"}, 201


@product_controller.route("/get/<int:id>", methods=["GET"])
@jwt_required()
@require_permission("read_product")
@require_product_from_same_company
@spectree.validate(
    resp=Response(
        HTTP_200=DetailProductResponse,
        HTTP_400=ErrorOutput
    ),
    tags=["Product"]
)
def detail_product(id: int):
    if not id:
        return {"error": "ID not provided"}, 400

    product = product_service.get_product_by_id(id)
    return {"product": product}, 200


@product_controller.route("/update/<int:id>", methods=["PATCH", "PUT"])
@jwt_required()
@require_permission("update_product")
@require_product_from_same_company
@spectree.validate(
    json=UpdateProductInputModel,
    resp=Response(
        HTTP_200=MessageResponse,
        HTTP_400=ErrorOutput
    ),
    tags=["Product"]
)
def update_product(json: UpdateProductInputModel, id: int):
    if not id:
        return {"error": "ID not provided"}, 400

    data = json.model_dump(exclude_unset=True)
    product_service.update_product(id, data)

    return {"msg": "Product updated successfully"}, 200


@product_controller.route("/deactivate/<int:id>", methods=["PATCH"])
@jwt_required()
@require_permission("delete_product")
@require_product_from_same_company
@spectree.validate(
    resp=Response(
        HTTP_200=MessageResponse,
        HTTP_400=ErrorOutput
    ),
    tags=["Product"]
)
def deactivate_product(id: int):
    if not id:
        return {"error": "ID not provided"}, 400

    data = {"status": "INACTIVE"}
    product_service.deactivate_product(id, data)

    return {"msg": "Product deactivated successfully"}, 200


@product_controller.route("/get/all", methods=["GET"])
@jwt_required()
@require_permission("read_product")
@spectree.validate(
    resp=Response(
        HTTP_200=ListDetailProductModel,
        HTTP_400=ErrorOutput
    ),
    tags=["Product"]
)
def get_all_products():
    user_company = get_current_user_company()
    company_id = user_company.company_id

    page = max(request.args.get('page', 1, type=int), 1)
    per_page = min(max(request.args.get('per_page', 10, type=int), 1), 100)
    search = request.args.get('search')

    products, total = product_service.get_products(company_id, page, per_page, search)


    return {
        "products": products,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": math.ceil(total / per_page) if total else 0
    }, 200


@product_controller.route("/search/<string:name>", methods=["GET"])
@jwt_required()
@require_permission("read_product")
@spectree.validate(
    resp=Response(
        HTTP_200=DetailProductResponse,
        HTTP_400=ErrorOutput
    ),
    tags=["Product"]
)
def get_product_by_name(name: str):
    user_company = get_current_user_company()
    company_id = user_company.company_id

    product = product_service.get_product_by_name(name, company_id)

    return {'product': product}, 200
