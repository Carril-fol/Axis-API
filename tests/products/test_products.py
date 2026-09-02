from tests.conftest import create_product, get_product, list_stock, make_category, make_product
from tests.products.conftest import deactivate_product, update_product


def test_creating_a_product_creates_its_stock(client, owner):
    product_id = make_product(client, owner, name="Laptop Pro", quantity=10)

    rows = list_stock(client, owner)

    assert len(rows) == 1
    assert rows[0]["product"]["id"] == product_id
    assert rows[0]["stock"]["quantity"] == 10


def test_update_a_product(client, owner):
    product_id = make_product(client, owner, name="Laptop Pro")

    response = update_product(
        client, owner, product_id, description="A much faster laptop"
    )

    assert response.status_code == 200
    product = get_product(client, owner, product_id)
    assert product.get_json()["product"]["description"] == "A MUCH FASTER LAPTOP"


def test_deactivating_a_product_empties_its_stock(client, owner):
    product_id = make_product(client, owner, name="Laptop Pro", quantity=25)

    response = deactivate_product(client, owner, product_id)

    assert response.status_code == 200
    assert list_stock(client, owner) == []


def test_a_role_without_the_permission_is_refused(client, owner, member):
    category_id = make_category(client, owner)

    response = create_product(client, member, name="Laptop Pro", category_id=category_id)

    assert response.status_code == 403


def test_another_company_cannot_read_a_product(client, owner, other_company):
    product_id = make_product(client, owner, name="Laptop Pro")

    response = get_product(client, other_company, product_id)

    assert response.status_code == 403
