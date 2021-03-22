from sqlalchemy import Column, String, Integer, ARRAY

from .base import db, BaseColumns


class City(db.Model, BaseColumns):
    __tablename__ = "city"

    name = Column(String(50), nullable=False, unique=True)  # 城市名
    spell = Column(String(100), server_default='')  # 拼写
    spell_short = Column(String(20), server_default='')  # 简拼
    keywords = Column(ARRAY(String), server_default='{}')  # 关键词，用于地区识别
    priority = Column(Integer, server_default='1')  # 级别
    code = Column(String(10), unique=True)  # 城市代码
    province_name = Column(String(30))  # 省份

    def as_dict(self, fields=None):
        detail = {
            "name": self.name,
            "code": self.code
        }

        if not fields:
            return detail
        return {attr: detail[attr] for attr in fields if attr in detail}
