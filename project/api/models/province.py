from sqlalchemy import Column, String, Integer, ARRAY

from .base import db, BaseColumns


class Province(db.Model, BaseColumns):
    __tablename__ = "province"

    name = Column(String(30), unique=True, nullable=False)
    spell = Column(String(100), server_default='')
    spell_short = Column(String(20), server_default='')
    keywords = Column(ARRAY(String), server_default='{}')
    priority = Column(Integer, server_default='1')
    code = Column(String(10), unique=True)

