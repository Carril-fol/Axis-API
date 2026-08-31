from shared.database.database import Database


def register_database_lifecycle(app):
    @app.after_request
    def _commit_or_rollback(response):
        if response.status_code < 400:
            Database.commit()
        else:
            Database.rollback()
        return response

    @app.teardown_appcontext
    def _close_session(exception=None):
        Database.remove()

    return app
