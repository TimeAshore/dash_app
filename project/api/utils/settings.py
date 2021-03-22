# services/isip/project/api/utils/settings.py

from flask_migrate import Migrate

from project.api.models import db, redis_store


def init_db(app):
    """
    Create database if doesn't exist and
    create all tables.
    """

    db.init_app(app)
    redis_store.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)
    return db


