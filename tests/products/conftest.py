def update_product(client, account, product_id: int, **fields):
    return client.patch(
        f"/products/api/v1/update/{product_id}", json=fields, headers=account.headers
    )


def deactivate_product(client, account, product_id: int):
    return client.patch(
        f"/products/api/v1/deactivate/{product_id}", headers=account.headers
    )
