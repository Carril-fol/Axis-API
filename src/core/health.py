from flask import Blueprint
from sqlalchemy import text

from shared.database.database import Database

health_blueprint = Blueprint("health", __name__)

@health_blueprint.route("/health", methods=["GET"])
def health():
    try:
        Database.session().execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    status = "ok" if db_status == "ok" else "degraded"
    return {"status": status, "db": db_status}, 200 if status == "ok" else 503
