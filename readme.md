# Stock Management API

A multi-tenant REST API for stock and inventory management. Each company manages its own products, categories, stock, and users through a role-based access control system.

## Why this project

Built as a portfolio project to practice designing a production-grade 
multi-tenant REST API from scratch. The goal was to implement patterns 
I'd use in a real backend: RBAC, tenant isolation, JWT with cookies, 
database migrations, and automated API docs — all in a single cohesive system.

## Tech Stack

- **Python 3.13** + **Flask**
- **SQLAlchemy** + **Alembic** (migrations)
- **PostgreSQL** (Neon serverless)
- **Flask-JWT-Extended** (authentication via cookies)
- **Pydantic v2** (request/response validation)
- **Spectree** (OpenAPI docs)
- **Argon2** (password hashing)
- **Pytest** (testing with SQLite in-memory)

## Project Structure

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

Each module follows the same structure: `entity`, `repository`, `service`, `model`, `controller`, `exceptions`, and optionally `middleware`.

## Setup

### Requirements

- Python 3.13+
- PostgreSQL database (or Neon connection string)

### Installation

```bash
git clone https://github.com/Carril-fol/stocky-api-rest.git
cd stocky-api-rest
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

### Environment variables

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

### Run

```bash
cd src
python app.py
```

On startup the server will:
1. Create all database tables
2. Seed all permissions

## API Overview

All endpoints are prefixed with their module version path. JWT is sent via HTTP-only cookies on login/register.

| Module | Prefix |
|---|---|
| Auth & Users | `/users/api/v1` |
| Company user management | `/users/api/v1` |
| Companies | `/companies/api/v1` |
| Roles | `/roles/api/v1` |
| Role permissions | `/role-permissions/api/v1` |
| Categories | `/categories/api/v1` |
| Products | `/products/api/v1` |
| Stock | `/stock/api/v1` |

Interactive API docs available at `/apidoc/swagger` once the server is running.

## Authentication

Registration creates a company and an OWNER user with all permissions assigned. Login returns a JWT access token (30 min) and refresh token (30 days) via cookies.

```
POST /users/api/v1/register   # Create company + owner user
POST /users/api/v1/login      # Get access + refresh tokens
POST /users/api/v1/refresh    # Rotate tokens
POST /users/api/v1/logout     # Clear cookies
GET  /users/api/v1/me         # Current user profile
```

## Authorization

Every protected endpoint uses two layers:

1. `@jwt_required()` — validates the JWT token
2. `@require_permission("permission_name")` — checks the user's role has the required permission (DB lookup per request)

Additionally, resource endpoints use `@require_user_from_same_company()` to enforce tenant isolation — users cannot access resources from other companies.

## Running Tests

Tests use SQLite in-memory and are fully isolated (DB is wiped between each test).

```bash
pytest
pytest -v                          # verbose
pytest tests/test_users.py -v      # specific file
```

## Migrations

```bash
alembic upgrade head                                    # apply migrations
alembic revision --autogenerate -m "description"        # generate new migration
```

## Quick start

The typical flow is: after registration or login, the server sets an authentication cookie. The client then uses that cookie automatically when making requests to protected endpoints.

All examples use `curl`. The `-c cookies.txt` flag saves the JWT cookie on login; `-b cookies.txt` sends it on subsequent requests.

### 1. Register (creates company + owner user)

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

### 2. Login

```bash
curl -s -X POST http://localhost:8000/users/api/v1/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "john@acme.com",
    "password": "secret123"
  }'
```

### 3. Create a product

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

### 4. List products

```bash
curl -s http://localhost:8000/products/api/v1/get/all \
  -b cookies.txt
```

### 5. Logout

```bash
curl -s -X POST http://localhost:8000/users/api/v1/logout \
  -b cookies.txt
```
