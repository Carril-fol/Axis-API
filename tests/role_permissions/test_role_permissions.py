from tests.conftest import make_role
from tests.role_permissions.conftest import (
    SEEDED_PERMISSIONS,
    assign_permission,
    granted,
    link_id,
    permission_id,
    revoke_permission,
    update_link,
)


def test_the_owner_role_holds_every_permission(client, owner):
    assert len(granted(client, owner, owner.role_id)) == SEEDED_PERMISSIONS


def test_a_granted_permission_takes_effect_on_the_next_request(client, owner, member):
    assert client.get("/products/api/v1/get/all", headers=member.headers).status_code == 403

    assign_permission(client, owner, member.role_id, [permission_id("read_product")])

    assert client.get("/products/api/v1/get/all", headers=member.headers).status_code == 200


def test_a_revoked_permission_stops_working_on_the_next_request(client, owner, member):
    assign_permission(client, owner, member.role_id, [permission_id("read_product")])

    revoke_permission(client, owner, member.role_id, permission_id("read_product"))

    assert client.get("/products/api/v1/get/all", headers=member.headers).status_code == 403


def test_update_swaps_the_permission_on_the_link(client, owner):
    role_id = make_role(client, owner, "Manager")
    assign_permission(client, owner, role_id, [permission_id("read_product")])

    response = update_link(
        client,
        owner,
        link_id(role_id, permission_id("read_product")),
        role_id=role_id,
        permission=permission_id("read_stock"),
    )

    assert response.status_code == 200
    assert granted(client, owner, role_id) == ["read_stock"]


def test_a_role_from_another_company_is_refused(client, owner, other_company):
    foreign_role_id = make_role(client, other_company, "Foreign")

    response = assign_permission(
        client, owner, foreign_role_id, [permission_id("read_product")]
    )

    assert response.status_code == 403
