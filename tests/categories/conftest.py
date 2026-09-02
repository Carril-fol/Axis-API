RESERVED_CATEGORY = "OTHER"


def get_category(client, account, category_id: int):
    return client.get(f"/categories/api/v1/get/{category_id}", headers=account.headers)


def search_category(client, account, name: str) -> dict:
    response = client.get(f"/categories/api/v1/search/{name}", headers=account.headers)
    return response.get_json()["category"]


def disable_category(client, account, category_id: int):
    return client.delete(
        f"/categories/api/v1/disable/{category_id}", headers=account.headers
    )
