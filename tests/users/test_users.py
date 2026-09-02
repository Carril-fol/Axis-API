from tests.conftest import create_company_user, list_users, make_role
from tests.users.conftest import delete_user


def test_create_a_user_for_the_company(client, owner):
    role_id = make_role(client, owner, "Manager")

    response = create_company_user(
        client, owner, email="peter@test.com", role_id=role_id,
        first_name="Peter", last_name="Jones",
    )

    assert response.status_code == 201
    created = next(u for u in list_users(client, owner) if u["email"] == "peter@test.com")
    assert created["role_id"] == role_id


def test_delete_a_user(client, owner, member):
    response = delete_user(client, owner, member.user_id)

    assert response.status_code == 200
    assert [u["id"] for u in list_users(client, owner)] == [owner.user_id]


def test_a_member_cannot_delete_the_owner(client, owner, member):
    response = delete_user(client, member, owner.user_id)

    assert response.status_code == 403


def test_users_are_not_shared_between_companies(client, owner, member, other_company):
    assert [u["id"] for u in list_users(client, other_company)] == [other_company.user_id]
