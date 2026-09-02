import json
from pathlib import Path

from shared.database.database import Database

from container import permission_service


def seed_permissions():
    path = Path(__file__).parent / "permissions.json"
    with open(path, "r") as f:
        data = json.load(f)

    with Database.transaction():
        existing = {p["name"] for p in permission_service.get_all_permissions()}

        for permission_name in data["permissions"]:
            if permission_name not in existing:
                permission_service.create_permission({"name": permission_name})
