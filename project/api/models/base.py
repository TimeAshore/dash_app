# services/isip/project/api/models/base.py
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, BigInteger, func, TIMESTAMP


db = SQLAlchemy()
redis_store = FlaskRedis()


class BaseColumns:
    id = Column(BigInteger(), primary_key=True, nullable=False, autoincrement=True, unique=True)
    create_time = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False, index=True)
    update_time = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False,
                         onupdate=func.current_timestamp(), index=True)
