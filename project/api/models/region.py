from sqlalchemy import Column, String, Integer, ARRAY

from .base import db, BaseColumns


class Region(db.Model, BaseColumns):
    __tablename__ = 'region'

    name = Column(String(30), nullable=False)  # 二级名称
    spell = Column(String(50), nullable=False)  # 拼写
    spell_short = Column(String(20), server_default='')  # 简拼
    priority = Column(Integer, server_default='1')  # 级别
    keywords = Column(ARRAY(String), server_default='{}')  # 关键词，用于地区识别
    code = Column(String(6), unique=True)  # 二级城市代码
    city_name = Column(String(30))  # 所属一级城市名

    def as_dict(self, fields=None):
        detail = {
            "name": self.name,
            "code": self.code,
            "city_name": self.city_name
        }

        if not fields:
            return detail
        return {attr: detail[attr] for attr in fields if attr in detail}
