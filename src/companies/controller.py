from flask import Blueprint
from flask_jwt_extended import jwt_required
from spectree import Response

from core.extensions import spectree
from shared.models import ErrorOutput, MessageResponse
from container import company_service
from shared.authz import get_current_user_company

from .model import (
    UpdateCompanyInput,
    DetailCompanyResponse
)


company_controller = Blueprint(
    'company_controller',
    __name__,
    url_prefix='/companies/api/v1'
)


@company_controller.route('/update/<int:company_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@spectree.validate(
    json=UpdateCompanyInput,
    resp=Response(
        HTTP_200=MessageResponse,
        HTTP_400=ErrorOutput
    ),
    tags=['Companies']
)
def update_company(json: UpdateCompanyInput, company_id: int):
    data = json.model_dump(exclude_unset=True)
    user_data = get_current_user_company()
    requesting_role_id = user_data.role_id

    company_service.update_company(company_id, data, requesting_role_id)
    return {"msg": "Company updated successfully"}, 200


@company_controller.route('/detail/<int:company_id>', methods=['GET'])
@jwt_required()
@spectree.validate(
    resp=Response(
        HTTP_200=DetailCompanyResponse,
        HTTP_400=ErrorOutput
    ),
    tags=['Companies']
)
def detail_company(company_id: int):
    user_data = get_current_user_company()
    requesting_role_id = user_data.role_id

    company = company_service.detail_company(company_id, requesting_role_id)
    return {"company": company}, 200
