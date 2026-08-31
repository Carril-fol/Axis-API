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

# Loading environment variables
load_dotenv()


# Flask
# https://flask.palletsprojects.com/en/stable/
app = Flask(__name__)

# Trust X-Forwarded-* headers from a single reverse proxy (nginx, cloudflare, etc.)
# so request.remote_addr reflects the real client IP instead of the proxy's.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Flask-JWT-Extended
# https://flask-jwt-extended.readthedocs.io/en/stable/
jwt = JWTManager(app)

# Flask-CORS
# https://flask-cors.readthedocs.io/en/latest/
cors = CORS(
    app, 
    supports_credentials=True,
    origins=[
        "http://localhost:3000"
    ],
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With", "application/json"]
)

# Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute", "1000 per hour"],
    storage_uri=os.getenv("REDIS_URL", "memory://")
)


# Spectree
spectree = SpecTree(
    'flask',
    title='Inventra API',
    version='1.0.0',
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

# Flask-Talisman
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
