from pathlib import Path

from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory

from shared.database.database import Database
from shared.seeds.permissions_seeder import seed_permissions


_ALEMBIC_DIR = Path(__file__).resolve().parents[2] / "alembic"


def _revisions() -> tuple[str | None, str | None]:
    try:
        with Database.session().get_bind().connect() as connection:
            applied = MigrationContext.configure(connection).get_current_revision()
    finally:
        Database.remove()

    return applied, ScriptDirectory(str(_ALEMBIC_DIR)).get_current_head()


def setup_database() -> None:
    Database.initialize()

    applied, head = _revisions()
    if applied != head:
        raise RuntimeError(
            "The database is at revision %s and the code expects %s. "
            "Run 'alembic upgrade head' before starting the app."
            % (applied or "none (no schema)", head)
        )

    seed_permissions()
