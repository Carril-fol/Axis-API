# Stock Management API

A multi-tenant REST API for stock and inventory management. Each company manages its own products, categories, stock, and users through a role-based access control system (RBAC).

## Tech Stack

Python 3.13 with Flask. SQLAlchemy and Alembic for data handling and migrations. PostgreSQL (Neon serverless) as the database. Authentication with Flask-JWT-Extended using cookies. Request and response validation with Pydantic v2. Automatic documentation with Spectree. Password hashing with Argon2. Testing with Pytest on an in-memory SQLite database.

## Project structure

```
src/
├── app.py                  # Flask app entry point
├── core/                   # Infrastructure (DB, extensions, settings)
├── modules/                # Domain modules
│   ├── users/
│   ├── users_companies/    # Auth helpers + company user management
│   ├── companies/
│   ├── roles/
│   ├── permissions/
│   ├── role_permissions/   # RBAC middleware
│   ├── categories/
│   ├── products/
│   └── stock/
└── seeds/                  # Permissions seeder
tests/                      # Pytest test suite
```

Each module follows the same structure: entity, repository, service, model, controller, exceptions, and optionally middleware.

## Setup

You need Python 3.13 or higher and a PostgreSQL database (or a Neon connection string).

```bash
git clone https://github.com/Carril-fol/stocky-api-rest.git
cd stocky-api-rest
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

```env
NEON_DATABASE_URL=postgresql://user:password@host/dbname
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
FLASK_ENV=development
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

To run the server:

```bash
cd src
python app.py
```

On startup, the server creates all database tables and loads the initial permissions.

## API

Each module has its own route prefix, all versioned:

Auth and users live under `/users/api/v1`, company user management is also under `/users/api/v1`, companies under `/companies/api/v1`, roles under `/roles/api/v1`, role permissions under `/role-permissions/api/v1`, categories under `/categories/api/v1`, products under `/products/api/v1`, and stock under `/stock/api/v1`.

Interactive documentation is available at `/apidoc/swagger` while the server is running.

## Authentication

Registration creates a company and an OWNER user with all permissions assigned. Login returns an access token (30 min) and a refresh token (30 days) via cookies.

```
POST /users/api/v1/register   # Creates company + owner user
POST /users/api/v1/login      # Returns access + refresh tokens
POST /users/api/v1/refresh    # Rotates the tokens
POST /users/api/v1/logout     # Clears the cookies
GET  /users/api/v1/me         # Current user profile
```

## Authorization

Every protected endpoint goes through two layers: `@jwt_required()` validates the token, and `@require_permission("permission_name")` checks that the user's role has the required permission. On top of that, resource endpoints use `@require_user_from_same_company()` to make sure a user can't access another company's data.

## Tests

Tests run on an in-memory SQLite database and are isolated from each other; the database is wiped between each test.

```bash
pytest
pytest -v                          # verbose
pytest tests/test_users.py -v      # specific file
```

## Migrations

```bash
alembic upgrade head                                    # apply migrations
alembic revision --autogenerate -m "description"         # generate a new migration
```

## Usage example

After registering or logging in, the server sets an authentication cookie that the client automatically uses on subsequent requests to protected endpoints.

The examples use curl. The `-c cookies.txt` flag saves the login cookie, and `-b cookies.txt` sends it on the following requests.

Register (creates company + owner user):

```bash
curl -s -X POST http://localhost:8000/users/api/v1/register \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "user": {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@acme.com",
      "password": "secret123",
      "confirm_password": "secret123"
    },
    "company": {
      "name": "Acme Corp",
      "country": "Argentina",
      "address": "Av. Corrientes 1234"
    }
  }'
```

Login:

```bash
curl -s -X POST http://localhost:8000/users/api/v1/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "john@acme.com",
    "password": "secret123"
  }'
```

Create a product:

```bash
curl -s -X POST http://localhost:8000/products/api/v1/create \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "Laptop Pro 15",
    "description": "High performance laptop",
    "category_id": 1,
    "quantity": 10
  }'
```

List products:

```bash
curl -s http://localhost:8000/products/api/v1/get/all \
  -b cookies.txt
```

Logout:

```bash
curl -s -X POST http://localhost:8000/users/api/v1/logout \
  -b cookies.txt
```
