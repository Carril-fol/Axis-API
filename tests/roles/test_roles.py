from tests.conftest import create_role, list_roles, list_users, make_role
from tests.roles.conftest import RESERVED_ROLE, assign_role, delete_role, get_role


def test_create_and_read_a_role(client, owner):
    role_id = make_role(client, owner, "Manager")

    response = get_role(client, owner, role_id)

    assert response.status_code == 200
    assert response.get_json()["name"] == "MANAGER"


def test_the_reserved_name_is_refused(client, owner):
    response = create_role(client, owner, RESERVED_ROLE.lower())

    assert response.status_code == 409


def test_deleting_a_role_moves_its_users_to_the_reserved_role(client, owner, member):
    delete_role(client, owner, member.role_id)

    moved = next(user for user in list_users(client, owner) if user["id"] == member.user_id)
    default_role = next(
        role for role in list_roles(client, owner) if role["name"] == RESERVED_ROLE
    )

    assert moved["role_id"] == default_role["id"]


def test_assign_a_role_to_a_user(client, owner, member):
    role_id = make_role(client, owner, "Supervisor")

    response = assign_role(client, owner, member.user_id, role_id)

    assert response.status_code == 200
    users = list_users(client, owner)
    assert next(u for u in users if u["id"] == member.user_id)["role_id"] == role_id


def test_a_role_from_another_company_cannot_be_assigned(client, owner, member, other_company):
    foreign_role_id = make_role(client, other_company, "Foreign")

    response = assign_role(client, owner, member.user_id, foreign_role_id)

    assert response.status_code == 404


def test_another_company_cannot_read_a_role(client, owner, other_company):
    role_id = make_role(client, owner, "Warehouse")

    response = get_role(client, other_company, role_id)

    assert response.status_code == 403


def test_a_role_without_the_permission_is_refused(client, member):
    response = create_role(client, member, "Manager")

    assert response.status_code == 403
