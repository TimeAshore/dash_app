from sqlalchemy import Column
from sqlalchemy import String

from .base import db, BaseColumns


class BanGroup(db.Model, BaseColumns):
    __tablename__ = "ban_group"
    name = Column(String(50), server_default='', unique=True)
    spell = Column(String(15), server_default='')

    def __init__(self, name):
        self.name = name

    def as_dict(self, **kwargs):
        return {'id': self.id,
                'name': self.name,
                'spell': self.spell
                }
