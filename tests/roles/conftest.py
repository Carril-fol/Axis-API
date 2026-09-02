RESERVED_ROLE = "DEFAULT"


def get_role(client, account, role_id: int):
    return client.get(f"/roles/api/v1/get/{role_id}", headers=account.headers)


def delete_role(client, account, role_id: int):
    return client.delete(f"/roles/api/v1/delete/{role_id}", headers=account.headers)


def assign_role(client, account, user_id: int, role_id: int):
    return client.patch(
        "/roles/api/v1/assign-role",
        json={"user_id": user_id, "role_id": role_id},
        headers=account.headers,
    )
