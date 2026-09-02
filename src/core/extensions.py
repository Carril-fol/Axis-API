import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
from spectree import SpecTree
from spectree.models import SecurityScheme
from flask_talisman import Talisman

load_dotenv()


app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

jwt = JWTManager(app)

cors = CORS(
    app, 
    supports_credentials=True,
    origins=[
        "http://localhost:3000"
    ],
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With", "application/json"]
)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute", "1000 per hour"],
    storage_uri=os.getenv("REDIS_URL", "memory://")
)


spectree = SpecTree(
    'flask',
    title='Axis API',
    version='1.0.0',
    description=(
        "Multi-tenant stock management API. Every resource is scoped to the company "
        "the authenticated user belongs to, so two companies never see each other's "
        "products, categories, stock, users or roles.\n\n"
        "**Authentication.** `POST /auth/api/v1/register` creates a company together "
        "with its owner; `POST /auth/api/v1/login` signs in an existing user. Both "
        "return a JWT in an httpOnly `access_token` cookie, which every other endpoint "
        "requires.\n\n"
        "**Authorization.** Role-based: a role owns a set of permissions and each user "
        "is assigned one role per company. A request without the required permission "
        "gets `403`.\n\n"
        "**Rate limits.** 60 requests per minute and 1000 per hour per IP by default, "
        "tightened to 3 per hour on register and 5 per minute on login. Exceeding a "
        "limit returns `429`.\n\n"
        "**Errors** are always JSON: `{\"error\": \"...\"}`, plus a `detail` "
        "field on HTTP errors raised by the framework."
    ),
    security_schemes=[
        SecurityScheme(
            name="AccessToken",
            data={
                "type": "apiKey",
                "in": "cookie",
                "name": "access_token" 
            },
        ),
    ],
    security={"AccessToken": []}
)

talisman = Talisman(
    app,
    force_https=False,
    strict_transport_security=False,
    strict_transport_security_max_age=31536000,
    strict_transport_security_include_subdomains=True,
    x_content_type_options=True,
    frame_options="SAMEORIGIN",
    content_security_policy=False,
)
