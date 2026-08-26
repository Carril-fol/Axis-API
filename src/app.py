from shared.config.asgi import start_server
from shared.config.settings import settings_from_server, type_server

from core.extensions import app, spectree
from core.health import health_blueprint
from core.error_handlers import register_error_handlers
import core.logger

from auth.error_handlers import register_auth_error_handlers

# from products.product_controller import product_controller
# from categories.category_controller import category_controller
# from products.stock_controller import stock_blueprint
# from companies.company_controller import company_controller
# from users.user_controller import users_blueprint
# from users_companies.users_companies_controller import users_companies_blueprint
# from roles.role_controller import role_blueprint
# from role_permissions.role_permission_controller import role_permission_controller
from auth.auth_controller import auth_blueprint

#Spectree
spectree.register(app)

# Error handlers
register_error_handlers(app)
register_auth_error_handlers(app)

# Flask
# https://flask.palletsprojects.com/en/3.0.x/
app.config.from_object(settings_from_server[type_server])

# Blueprints
# app.register_blueprint(product_controller)
# app.register_blueprint(category_controller)
# app.register_blueprint(stock_blueprint)
# app.register_blueprint(users_blueprint)
# app.register_blueprint(users_companies_blueprint)
# app.register_blueprint(company_controller)
# app.register_blueprint(role_blueprint)
# app.register_blueprint(role_permission_controller)
app.register_blueprint(health_blueprint)
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    start_server(app)