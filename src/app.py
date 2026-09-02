from shared.config.wsgi import start_server
from shared.config.settings import settings_from_server, type_server

import core.logger
from core.extensions import app, jwt, spectree
from core.health import health_blueprint
from core.error_handlers import register_error_handlers, register_jwt_error_handlers
from core.database_lifecycle import register_database_lifecycle


from products.controller import product_controller
from categories.controller import category_controller
from stock.controller import stock_blueprint
from companies.controller import company_controller
from users.controller import users_blueprint
from users_companies.controller import users_companies_blueprint
from roles.controller import role_blueprint
from role_permissions.controller import role_permission_controller
from auth.controller import auth_blueprint

spectree.register(app)


register_error_handlers(app)
register_jwt_error_handlers(jwt)

register_database_lifecycle(app)

app.config.from_object(settings_from_server[type_server])


app.register_blueprint(product_controller)
app.register_blueprint(category_controller)
app.register_blueprint(stock_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(users_companies_blueprint)
app.register_blueprint(company_controller)
app.register_blueprint(role_blueprint)
app.register_blueprint(role_permission_controller)
app.register_blueprint(health_blueprint)
app.register_blueprint(auth_blueprint)


@app.route('/', methods=["GET"])
def default():
    return {"msg": {
        "status": "ok",
        "docs": "/apidoc/swagger"
    }}

if __name__ == "__main__":
    start_server(app)
