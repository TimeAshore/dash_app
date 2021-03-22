# services/socamas/project/__init__.py

import os
from flask import Flask

from project.api.utils.logger import Logging

# from project.api.utils.middleware import \
#     before_request_middleware, after_request_middleware, teardown_appcontext_middleware
#
# from project.api.utils.middleware import response

from project.api.utils.routers import register_routes as init_routes

from project.api.utils.settings import init_db

from project.config import DevelopmentConfig

from project.api.utils.responses import app_error_handler, JSONResponse


def create_app(script_info=None):
    """Create Flask app."""

    # initialize flask application
    app = Flask(__name__, template_folder='templates', static_folder='static')
    # app_settings = os.getenv('APP_SETTINGS')
    app_settings = DevelopmentConfig
    app.config.from_object(app_settings)

    # register all blueprints
    init_routes(app=app)

    # register JWT
    # init_jwt(app=app)

    # register system logger
    # Logging(app=app)

    # init sentry
    # sentry.init_app(app, dsn=app.config.get('SENTRY_DSN'),
    #                 logging=True, level=logging.ERROR)

    # register custom response class
    app.response_class = JSONResponse

    app_error_handler(app=app)

    # register before request middleware
    # before_request_middleware(app=app)

    # register after request middleware
    # after_request_middleware(app=app)

    # register after app context teardown middleware
    # teardown_appcontext_middleware(app=app)

    # register custom error handler
    # response.app_error_handler(app=app)

    # register session for auth token
    # db_redis.init_app(app)

    # initialize the database
    app_db = init_db(app=app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': app_db}
    return app
