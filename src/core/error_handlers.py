from flask import Flask, jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from shared.exceptions import AppException


def _constraint_violado(error: IntegrityError) -> str | None:
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
            "IntegrityError (constraint=%s): %s", _constraint_violado(error), error.orig
        )
        return jsonify({"error": "The operation conflicts with existing data"}), 409

    @app.errorhandler(Exception)
    def handle_unhandled_exception(error: Exception):
        app.logger.exception("Unhandled exception: %s", error)
        return jsonify({"error": "Internal server error"}), 500
