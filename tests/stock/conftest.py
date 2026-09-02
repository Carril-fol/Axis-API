from tests.conftest import list_stock, make_product

LOW_STOCK_THRESHOLD = 10


def make_stock(
    client,
    account,
    name: str = "Test Product",
    quantity: int = 5,
    category_id: int | None = None,
) -> int:
    make_product(client, account, name=name, quantity=quantity, category_id=category_id)

    return next(
        row["stock"]["id"]
        for row in list_stock(client, account)
        if row["product"]["name"] == name.upper()
    )


def get_stock(client, account, stock_id: int):
    return client.get(f"/stock/api/v1/get/{stock_id}", headers=account.headers)


def update_stock(client, account, stock_id: int, quantity: int):
    return client.patch(
        f"/stock/api/v1/update/{stock_id}",
        json={"quantity": quantity},
        headers=account.headers,
    )


def list_low_stock(client, account) -> list[dict]:
    return client.get("/stock/api/v1/get/low", headers=account.headers).get_json()["data"]
