import pytest

from tests.conftest import make_category
from tests.stock.conftest import (
    LOW_STOCK_THRESHOLD,
    get_stock,
    list_low_stock,
    make_stock,
    update_stock,
)


def test_a_stock_row_comes_back_with_its_product(client, owner):
    stock_id = make_stock(client, owner, name="Laptop Pro", quantity=25)

    response = get_stock(client, owner, stock_id)

    body = response.get_json()["data"]
    assert response.status_code == 200
    assert body["stock"]["quantity"] == 25
    assert body["product"]["name"] == "LAPTOP PRO"


@pytest.mark.parametrize("quantity, expected", [
    (0, "OUT OF STOCK"),
    (LOW_STOCK_THRESHOLD - 1, "LOW STOCK"),
    (LOW_STOCK_THRESHOLD, "IN STOCK"),
])
def test_the_status_follows_the_quantity(client, owner, quantity, expected):
    stock_id = make_stock(client, owner, name="Laptop Pro", quantity=quantity)

    response = get_stock(client, owner, stock_id)

    assert response.get_json()["data"]["stock"]["status"] == expected


def test_update_the_quantity(client, owner):
    stock_id = make_stock(client, owner, name="Laptop Pro", quantity=5)

    response = update_stock(client, owner, stock_id, quantity=20)

    assert response.status_code == 200
    detail = get_stock(client, owner, stock_id)
    assert detail.get_json()["data"]["stock"]["quantity"] == 20


def test_low_stock_only_returns_what_is_under_the_threshold(client, owner):
    category_id = make_category(client, owner)
    make_stock(
        client, owner, name="Full", quantity=LOW_STOCK_THRESHOLD + 5, category_id=category_id
    )
    make_stock(client, owner, name="Low", quantity=3, category_id=category_id)

    rows = list_low_stock(client, owner)

    assert len(rows) == 1
    assert rows[0]["product"]["name"] == "LOW"


def test_another_company_cannot_read_a_stock_row(client, owner, other_company):
    stock_id = make_stock(client, owner, name="Laptop Pro")

    response = get_stock(client, other_company, stock_id)

    assert response.status_code == 403
