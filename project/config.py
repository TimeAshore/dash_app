# services/socamas/project/config.py

import os


class BaseConfig:
    """Base configuration"""

    # Root path of project
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    EXPORT_PATH = './project/api/data/export'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SECRET_KEY = os.environ.get("SECRET_KEY")
    SECRET_KEY = 'my_precious'

    # Redis_configuration
    # REDIS_URL = os.environ.get("REDIS_URL")


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    JSON_AS_ASCII = False

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@127.0.0.1/socamas"
    MESSAGE_QUEUE = "amqp://test_socweb:test_socweb@127.0.0.1/test_socweb"
    # MESSAGE_QUEUE = "'redis://192.168.199.221/3'"
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # MESSAGE_QUEUE = os.environ.get('MESSAGE_QUEUE')


class TestingConfig(BaseConfig):
    """Testing configuration"""

    TESTING = True
    REDIS_URL = "redis://:socamas@redis@socamas-redis:6379/1"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    ALEMBIC_CONFIG = "{}/migrations/alembic.ini".format(BaseConfig.PROJECT_PATH)


class ProductionConfig(BaseConfig):
    """Production configuration"""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

