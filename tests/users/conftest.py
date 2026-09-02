def delete_user(client, account, user_id: int):
    return client.delete(
        f"/users/api/v1/delete-user-from-company/{user_id}", headers=account.headers
    )
