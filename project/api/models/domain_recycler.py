# services/isip/project/api/models/domain_recycler.py
from sqlalchemy import Column, String, TIMESTAMP, Boolean, Integer
from .base import db, BaseColumns


class DomainRecycler(db.Model, BaseColumns):
    __tablename__ = "domain_recycler"

    def __init__(self, **kwargs):
        for attr in ['name', 'national_level', 'city_code', 'region_code', 'icp_updated', 'invalid_time', 'industries'
                     'icp_number', 'icp_source', 'sponsor', 'sponsor_type', 'tags', 'subdomain_count', 'website_count',
                     'reason']:
            if kwargs.get(attr) is not None:
                setattr(self, attr, kwargs[attr])

    name = Column(String(50), unique=True, nullable=False)  # 域名
    city_code = Column(String(50))  # 一级归属地
    region_code = Column(String(100))  # 二级归属地

    icp_number = Column(String(50), server_default='')  # 备案号
    icp_updated = Column(TIMESTAMP)  # 最后更新时间
    icp_source = Column(String(30), server_default='')  # 备案来源

    sponsor = Column(String(254), server_default='', index=True)  # 备案单位
    sponsor_type = Column(String(50), server_default='', index=True)  # 单位性质
    invalid_time = Column(TIMESTAMP)  # 失效时间

    industries = Column(String(50), server_default='', index=True)  # 行业
    national_level = Column(Boolean, server_default='0')  # 国家级
    tags = Column(String(50), server_default='', index=True)  # 标签

    subdomain_count = Column(Integer, server_default='0')  # 子域名数量
    website_count = Column(Integer, server_default='0')  # 网站数量
    website_count_updated = Column(TIMESTAMP)  # 网站数量更新时间

    reason = Column(String(254), server_default='')  # 删除原因

    def as_dict(self, fields=None):
        detail = {
            "id": self.id,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "name": self.name,
            "city_code": self.city_code,
            "region_code": self.region_code,
            "icp_number": self.icp_number,
            "icp_updated": self.icp_updated.strftime("%Y-%m-%d %H:%M:%S") if self.icp_updated else None,
            "icp_source": self.icp_source,
            "sponsor": self.sponsor,
            "sponsor_type": self.sponsor_type,
            "invalid_time": self.invalid_time.strftime("%Y-%m-%d %H:%M:%S") if self.invalid_time else None,
            "industries": self.industries,
            "national_level": self.national_level,
            "tags": self.tags,
            "subdomain_count": self.subdomain_count,
            "website_count": self.website_count,
            "website_count_updated": self.website_count_updated.strftime("%Y-%m-%d %H:%M:%S") if self.website_count_updated else None,
        }
        if not fields:
            return detail
        return {attr: detail[attr] for attr in fields if attr in detail}
