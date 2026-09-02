from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from shared.exceptions import AppException


def _violated_constraint(error: IntegrityError) -> str | None:
    diag = getattr(getattr(error, "orig", None), "diag", None)
    return getattr(diag, "constraint_name", None)


def register_error_handlers(app: Flask) -> None:

    @app.errorhandler(AppException)
    def handle_app_exception(error: AppException):
        return jsonify({"error": str(error)}), error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        return jsonify({"error": error.name, "detail": error.description}), error.code

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error: IntegrityError):
        app.logger.warning(
            "IntegrityError (constraint=%s): %s", _violated_constraint(error), error.orig
        )
        return jsonify({"error": "The operation conflicts with existing data"}), 409

    @app.errorhandler(Exception)
    def handle_unhandled_exception(error: Exception):
        app.logger.exception("Unhandled exception: %s", error)
        return jsonify({"error": "Internal server error"}), 500


def register_jwt_error_handlers(jwt: JWTManager) -> None:
    """flask-jwt-extended answers with {"msg": ...}; the API contract is {"error": ...},
    so every rejection it raises is rewritten here. A malformed token answers 401 like
    the rest, leaving 422 to mean request-body validation only."""

    @jwt.unauthorized_loader
    def handle_missing_token(reason: str):
        return jsonify({"error": reason}), 401

    @jwt.invalid_token_loader
    def handle_invalid_token(reason: str):
        return jsonify({"error": reason}), 401

    @jwt.expired_token_loader
    def handle_expired_token(_header, _payload):
        return jsonify({"error": "Token has expired"}), 401

    @jwt.revoked_token_loader
    def handle_revoked_token(_header, _payload):
        return jsonify({"error": "Token has been revoked"}), 401

    @jwt.needs_fresh_token_loader
    def handle_stale_token(_header, _payload):
        return jsonify({"error": "Fresh token required"}), 401
