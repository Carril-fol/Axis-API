from typing import NamedTuple

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool

from shared.database.database import Base, Database

_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
Database._engine = _engine
Database._session_factory = sessionmaker(
    bind=_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)
Database._scoped_session = scoped_session(Database._session_factory)

from app import app as flask_app
from container import user_company_service, user_service
from core.extensions import limiter
from shared.seeds.permissions_seeder import seed_permissions

Base.metadata.create_all(bind=_engine)

flask_app.config.update({
    "TESTING": True,
    "JWT_SECRET_KEY": "test-secret-key",
    "JWT_TOKEN_LOCATION": ["headers"],
    "JWT_COOKIE_CSRF_PROTECT": False,
    "JWT_COOKIE_SECURE": False,
    "RATELIMIT_ENABLED": False,
})
limiter.enabled = False


OWNER = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "owner@test.com",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!",
}

COMPANY = {
    "name": "Test Corp",
    "country": "Argentina",
    "address": "123 Main St",
}


class Account(NamedTuple):
    token: str
    headers: dict
    user_id: int
    company_id: int
    role_id: int


@pytest.fixture
def client():
    return flask_app.test_client()


@pytest.fixture(autouse=True)
def clean_db():
    Database.remove()
    session = Database.session()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    Database.remove()

    seed_permissions()
    yield
    Database.remove()


def register_request(client, user: dict = OWNER, company: dict = COMPANY):
    return client.post("/auth/api/v1/register", json={"user": user, "company": company})


def login(client, email: str = OWNER["email"], password: str = OWNER["password"]):
    return client.post("/auth/api/v1/login", json={"email": email, "password": password})


def create_role(client, account, name: str):
    return client.post(
        "/roles/api/v1/create-role", json={"name": name}, headers=account.headers
    )


def create_category(client, account, name: str):
    return client.post(
        "/categories/api/v1/create", json={"name": name}, headers=account.headers
    )


def create_product(client, account, name: str, category_id: int, quantity: int = 5):
    return client.post("/products/api/v1/create", json={
        "name": name,
        "description": "A test product",
        "category_id": category_id,
        "quantity": quantity,
    }, headers=account.headers)


def create_company_user(
    client,
    account,
    email: str,
    role_id: int,
    password: str = "SecurePass123!",
    first_name: str = "Mary",
    last_name: str = "Smith",
):
    return client.post("/users/api/v1/create-user-from-company", json={
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "confirm_password": password,
        "role_id": role_id,
    }, headers=account.headers)


def get_product(client, account, product_id: int):
    return client.get(f"/products/api/v1/get/{product_id}", headers=account.headers)


def list_roles(client, account) -> list[dict]:
    return client.get("/roles/api/v1/get-roles", headers=account.headers).get_json()["data"]


def list_users(client, account) -> list[dict]:
    response = client.get("/users/api/v1/get-users-from-company", headers=account.headers)
    return response.get_json()["users"]


def list_categories(client, account) -> list[dict]:
    response = client.get("/categories/api/v1/get/all", headers=account.headers)
    return response.get_json()["categories"]


def list_stock(client, account) -> list[dict]:
    return client.get("/stock/api/v1/get/all", headers=account.headers).get_json()["data"]


def register(client, email: str = OWNER["email"], company_name: str = COMPANY["name"]) -> Account:
    response = register_request(
        client, user={**OWNER, "email": email}, company={**COMPANY, "name": company_name}
    )
    assert response.status_code == 201, response.get_json()

    token = response.get_json()["access_token"]
    user = user_service.get_user_by_email(email)
    membership = user_company_service.get_membership_by_user_id(user.id)

    return Account(
        token=token,
        headers={"Authorization": f"Bearer {token}"},
        user_id=user.id,
        company_id=membership.company_id,
        role_id=membership.role_id,
    )


def make_role(client, account, name: str = "Warehouse") -> int:
    response = create_role(client, account, name)
    assert response.status_code == 201, response.get_json()

    return next(
        role["id"] for role in list_roles(client, account) if role["name"] == name.upper()
    )


def make_category(client, account, name: str = "Electronics") -> int:
    response = create_category(client, account, name)
    assert response.status_code == 201, response.get_json()

    return next(
        c["id"] for c in list_categories(client, account) if c["name"] == name.upper()
    )


def make_product(
    client,
    account,
    name: str = "Test Product",
    quantity: int = 5,
    category_id: int | None = None,
) -> int:
    response = create_product(
        client,
        account,
        name=name,
        category_id=category_id or make_category(client, account),
        quantity=quantity,
    )
    assert response.status_code == 201, response.get_json()

    found = client.get(f"/products/api/v1/search/{name}", headers=account.headers)
    return found.get_json()["product"]["id"]


@pytest.fixture
def owner(client) -> Account:
    return register(client)


@pytest.fixture
def other_company(client) -> Account:
    return register(client, email="owner_b@test.com", company_name="Company B")


@pytest.fixture
def member(client, owner) -> Account:
    email = "member@test.com"
    password = "SecurePass123!"
    role_id = make_role(client, owner, "Warehouse")

    response = create_company_user(client, owner, email=email, role_id=role_id, password=password)
    assert response.status_code == 201, response.get_json()

    token = login(client, email=email, password=password).get_json()["access_token"]

    return Account(
        token=token,
        headers={"Authorization": f"Bearer {token}"},
        user_id=user_service.get_user_by_email(email).id,
        company_id=owner.company_id,
        role_id=role_id,
    )
