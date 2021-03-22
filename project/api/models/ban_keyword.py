from sqlalchemy import Column
from sqlalchemy import String

from .base import db, BaseColumns


class BanKeyword(db.Model, BaseColumns):
    __tablename__ = "ban_keyword"

    def __init__(self, keyword, group, typ='keyword'):
        self.keyword = keyword
        self.typ = typ
        self.group = group

    typ = Column(String(10), server_default='keyword')
    keyword = Column(String(200), server_default='')
    group = Column(String(50), server_default='')

    def as_dict(self, **kwargs):
        return {'id': self.id,
                'keyword': self.keyword,
                'typ': self.typ,
                'group': self.group
                }
