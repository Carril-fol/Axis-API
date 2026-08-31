import json
from pathlib import Path

from permissions.exceptions import PermissionNotFound
from shared.database.database import Database

from container import permission_service


def seed_permissions():
    path = Path(__file__).parent / "permissions.json"
    with open(path, "r") as f:
        data = json.load(f)

    with Database.transaction():
        for permission_name in data["permissions"]:
            try:
                permission_service.get_permission_by_name(permission_name)
            except PermissionNotFound:
                permission_service.create_permission({"name": permission_name})
