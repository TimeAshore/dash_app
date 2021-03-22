from sqlalchemy import Column, String, Integer, ARRAY, TIMESTAMP, BigInteger

from .base import db, BaseColumns


class WebsiteRecycler(db.Model, BaseColumns):
    __tablename__ = "website_recycler"

    def __init__(self, **kwargs):
        for attr in ['url', 'domain', 'domain_id', 'city_code', 'region_code', 'ip', 'ip_area', 'title', 'web_type'
                     'host_dept', 'industries', 'ai_industries', 'tags', 'code_language', 'http_status',
                     'http_status_list', 'category', 'reason']:
            if kwargs.get(attr) is not None:
                setattr(self, attr, kwargs[attr])

    url = Column(String(254), nullable=False, unique=True, index=True)  # 网站地址
    domain = Column(String(100), nullable=False, index=True)  # 主域名
    domain_id = Column(BigInteger, nullable=False)  # 主域名ID
    city_code = Column(String(50))  # 一级归属地
    region_code = Column(String(100))  # 二级归属地

    ip = Column(String(50), nullable=False, index=True)  # IP地址
    ip_area = Column(String(254), server_default='')  # IP归属地

    title = Column(String(254), server_default='')  # 标题
    web_type = Column(String(30), server_default='', nullable=False, index=True)  # 网站类型
    host_dept = Column(String(254), server_default='')  # 归属单位
    host_type = Column(String(50), server_default='')  # 单位性质

    industries = Column(ARRAY(String), server_default='{}', index=True)  # 行业
    ai_industries = Column(ARRAY(String), server_default='{}', index=True)  # 智能分类行业

    tags = Column(ARRAY(String), server_default='{}')  # 标签
    code_language = Column(String(50), server_default='')  # 编程语言
    http_status = Column(Integer(), server_default='-1', index=True)  # http status
    http_status_list = Column(String(254), server_default='')  # http status list
    category = Column(String(50), server_default='', index=True)  # 类别

    reason = Column(String(254), server_default='')  # 删除原因

    def as_dict(self, fields=None):
        detail = {
            "id": self.id,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "url": self.url,
            "city_code": self.city_code,
            "region_code": self.region_code,
            "domain_id": self.domain_id,
            "domain": self.domain,
            "ip": self.ip,
            "ip_area": self.ip_area,
            "title": self.title,
            "web_type": self.web_type,
            "host_dept": self.host_dept,
            "host_type": self.host_type,
            "industries": self.industries,
            "ai_industries": self.ai_industries,
            "tags": self.tags,
            "code_language": self.code_language,
            "http_status": self.http_status,
            "http_status_list": self.http_status_list,
            "category": self.category
        }

        if not fields:
            return detail
        return {attr: detail[attr] for attr in fields if attr in detail}



