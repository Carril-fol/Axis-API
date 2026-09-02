from tests.categories.conftest import (
    RESERVED_CATEGORY,
    disable_category,
    get_category,
    search_category,
)
from tests.conftest import create_category, get_product, list_categories, make_category, make_product


def test_create_and_read_a_category(client, owner):
    category_id = make_category(client, owner, "Drinks")

    response = get_category(client, owner, category_id)

    assert response.status_code == 200
    assert response.get_json()["category"]["name"] == "DRINKS"


def test_the_reserved_name_is_refused(client, owner):
    response = create_category(client, owner, RESERVED_CATEGORY.lower())

    assert response.status_code == 409


def test_disabling_moves_the_products_to_the_reserved_category(client, owner):
    category_id = make_category(client, owner, "Drinks")
    product_id = make_product(client, owner, name="Cola", category_id=category_id)

    disable_category(client, owner, category_id)

    product = get_product(client, owner, product_id)
    fallback = search_category(client, owner, RESERVED_CATEGORY)

    assert product.get_json()["product"]["category_id"] == fallback["id"]


def test_a_role_without_the_permission_is_refused(client, member):
    response = create_category(client, member, "Drinks")

    assert response.status_code == 403


def test_categories_are_not_shared_between_companies(client, owner, other_company):
    make_category(client, owner, "Drinks")

    assert list_categories(client, other_company) == []
