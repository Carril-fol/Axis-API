from datetime import timedelta
from flask import Blueprint, make_response
from spectree import Response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    unset_access_cookies,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies
)

from core.extensions import limiter, spectree
from shared.models import ErrorOutput, MessageResponse
from .model import (
    RegisterWithCompanyInput,
    LoginInput,
    AuthOutput
)
from container import auth_service, user_registration_orchestrator


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth/api/v1")


@auth_blueprint.route("/register", methods=["POST"])
@limiter.limit("3 per hour")
@spectree.validate(
    json=RegisterWithCompanyInput,
    resp=Response(
        HTTP_201=AuthOutput,
        HTTP_400=ErrorOutput,
        HTTP_429=ErrorOutput,
    ),
    tags=["Auth"]
)
def register(json: RegisterWithCompanyInput):
    identity = user_registration_orchestrator.register_owner(
        json.user.model_dump(),
        json.company.model_dump(),
    )
    access_token = create_access_token(identity=str(identity), expires_delta=timedelta(minutes=30))

    response = make_response({"msg": "Register successful", "access_token": access_token}, 201)
    set_access_cookies(response, access_token)
    return response


@auth_blueprint.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
@spectree.validate(
    json=LoginInput,
    resp=Response(
        HTTP_200=AuthOutput,
        HTTP_401=ErrorOutput,
        HTTP_429=ErrorOutput
    ),
    tags=["Auth"],
)
def login(json: LoginInput):
    user_id = auth_service.authenticate(json)

    access_token = create_access_token(str(user_id))
    refresh_token = create_refresh_token(str(user_id))

    response = make_response({"msg": "Login successful", "access_token": access_token}, 200)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response


@auth_blueprint.route("/logout", methods=["POST"])
@jwt_required()
@spectree.validate(
    resp=Response(
        HTTP_200=MessageResponse,
        HTTP_401=ErrorOutput
    ),
    tags=["Auth"]
)
def logout():
    response = make_response({"msg": "Logout successfully"}, 200)
    unset_access_cookies(response)
    unset_jwt_cookies(response)
    return response


@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(verify_type=True, refresh=True)
@spectree.validate(
    resp=Response(
        HTTP_200=AuthOutput,
        HTTP_401=ErrorOutput
    ),
    tags=["Auth"]
)
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    new_refresh_token = create_refresh_token(identity=current_user)

    response = make_response({
        "msg": "Token refreshed",
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }, 200)
    set_access_cookies(response, new_access_token)
    set_refresh_cookies(response, new_refresh_token)
    return response
