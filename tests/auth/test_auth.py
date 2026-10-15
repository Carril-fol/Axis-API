from tests.auth.conftest import refresh
from tests.conftest import OWNER, login, register_request


def test_register_returns_a_token(client):
    response = register_request(client)

    assert response.status_code == 201


def test_register_rejects_a_duplicate_email(client, owner):
    response = register_request(client)

    assert response.status_code == 409


def test_login_returns_a_token(client, owner):
    response = login(client)

    assert response.status_code == 200
    assert response.get_json()["access_token"]


def test_login_rejects_a_wrong_password(client, owner):
    response = login(client, password="WrongPassword123!")

    assert response.status_code == 401


def test_refresh_rotates_both_tokens(client, owner):
    login(client)
    refresh_token = client.get_cookie("refresh_token_cookie").value

    response = refresh(client, refresh_token)

    assert response.status_code == 200
    body = response.get_json()
    assert body["access_token"]
    assert body["refresh_token"] != refresh_token


def test_a_protected_endpoint_needs_a_token(client):
    response = client.get("/roles/api/v1/get-roles")

    assert response.status_code == 401


def test_me_returns_the_user_role_and_permissions(client, owner):
    response = client.get("/auth/api/v1/me", headers=owner.headers)

    assert response.status_code == 200
    body = response.get_json()
    assert body["user"]["id"] == owner.user_id
    assert body["user"]["email"] == OWNER["email"]
    assert "password" not in body["user"]
    assert body["company_id"] == owner.company_id
    assert body["role"] == {"id": owner.role_id, "name": "OWNER", "status": "ACTIVE"}
    assert "create_user" in body["permissions"]


def test_me_gives_a_fresh_role_only_its_own_permissions(client, member):
    response = client.get("/auth/api/v1/me", headers=member.headers)

    assert response.status_code == 200
    body = response.get_json()
    assert body["role"]["name"] == "WAREHOUSE"
    assert body["permissions"] == []


def test_me_needs_a_token(client):
    response = client.get("/auth/api/v1/me")

    assert response.status_code == 401
