from sqlalchemy import Column, String, Integer

from .base import db, BaseColumns


class Industry(db.Model, BaseColumns):
    __tablename__ = 'industry'

    def __init__(self, **kwargs):
        for attr in ['name', 'website_count', 'spell']:
            if kwargs.get(attr):
                setattr(self, attr, kwargs[attr])

    name = Column(String(50), nullable=False, unique=True)  # 行业名称
    spell = Column(String(30), nullable=True, server_default='')  # 简拼
    website_count = Column(Integer, server_default='0')  # 网站数量

    def as_dict(self, fields=None):
        detail = {
            "name": self.name,
            "website_count": self.website_count
        }

        if not fields:
            return detail
        return {attr: detail[attr] for attr in fields if attr in detail}
