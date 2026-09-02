from sqlalchemy import inspect

from shared.database.database import Database
from shared.seeds.permissions_seeder import seed_permissions


def _has_schema() -> bool:
    try:
        return inspect(Database.session().get_bind()).has_table("permissions")
    finally:
        Database.remove()


def setup_database() -> None:
    Database.initialize()

    if not _has_schema():
        raise RuntimeError(
            "The database has no schema. Run 'alembic upgrade head' before starting the app."
        )

    seed_permissions()
