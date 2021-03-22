from sqlalchemy import Column, String, ARRAY, Integer

from project.api.models.base import db, BaseColumns


class UnitRecycler(db.Model, BaseColumns):
    __tablename__ = "unit_recycler"
    name = Column(String(100), nullable=False, unique=True)
    spell = Column(String(50), server_default='')
    category = Column(String(50), server_default='')
    tags = Column(ARRAY(String), server_default='{}')
    city = Column(String(100), server_default='')
    region = Column(String(100), server_default='')
    domain = Column(String(200), server_default='')
    domains = Column(ARRAY(String), server_default='{}')
    keywords = Column(ARRAY(String), server_default='{}')
    website_count = Column(Integer, server_default='0')
    reason = Column(String(254), server_default='')  # 删除原因

    def as_dict(self, fields=None):
        detail = {
            'id': self.id,
            'spell': self.spell,
            'keywords': self.keywords,
            'name': self.name,
            'category': self.category,
            'domains': self.domains,
            'tags': self.tags,
            'city': self.city,
            'region': self.region,
            'website_count': self.website_count,
            'reason': self.reason
        }

        if not fields:
            return detail
        return {attr: detail[attr] for attr in fields if attr in detail}
