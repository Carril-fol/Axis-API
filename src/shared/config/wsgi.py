from waitress import serve

from ..bootstrap import setup_database
from .settings import Config, type_server


def start_server(app):
    setup_database()

    host = Config.SERVER_HOST or "0.0.0.0"
    app.logger.info("Server listening on http://%s:%s", host, Config.SERVER_PORT)
    if host == "0.0.0.0":
        app.logger.info("Local: http://127.0.0.1:%s", Config.SERVER_PORT)
    app.logger.info("Environment: %s", type_server)

    serve(app, host=host, port=Config.SERVER_PORT)
