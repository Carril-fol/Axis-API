from container import permission_repository, role_permissions_repository

SEEDED_PERMISSIONS = 24


def permission_id(name: str) -> int:
    return permission_repository.get_permission_by_name(name).id


def link_id(role_id: int, permission: int) -> int:
    return role_permissions_repository.get_role_permission(role_id, permission).id


def granted(client, account, role_id: int) -> list[str]:
    response = client.get(
        f"/role-permissions/api/v1/get/{role_id}", headers=account.headers
    )
    return response.get_json()["permissions"]


def assign_permission(client, account, role_id: int, permission_ids: list[int]):
    return client.post("/role-permissions/api/v1/assign-permission-to-role", json={
        "role_id": role_id,
        "permission_id": permission_ids,
    }, headers=account.headers)


def revoke_permission(client, account, role_id: int, permission: int):
    return client.delete(
        f"/role-permissions/api/v1/revoke?role_id={role_id}&permission_id={permission}",
        headers=account.headers,
    )


def update_link(client, account, link: int, role_id: int, permission: int):
    return client.patch(
        f"/role-permissions/api/v1/update/{link}",
        json={"role_id": role_id, "permission_id": permission},
        headers=account.headers,
    )
