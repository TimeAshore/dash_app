from sqlalchemy import Column, String, ForeignKey, Boolean, Integer, ARRAY, TIMESTAMP, BigInteger, TEXT

from .base import db, BaseColumns


class WebsiteDuplicated(db.Model, BaseColumns):
    __tablename__ = "website_duplicated"

    def __init__(self, **kwargs):
        for attr in ['url', 'domain', 'domain_id', 'city_code', 'region_code', 'ip', 'ip_area', 'title', 'web_type'
                     'host_dept', 'host_type', 'industries', 'ai_industries', 'tags', 'code_language', 'http_status',
                     'http_status_list', 'category', 'is_auto']:
            if kwargs.get(attr) is not None:
                setattr(self, attr, kwargs[attr])

    url = Column(String(254), nullable=False, unique=True, index=True)  # 网址
    effective_url = Column(TEXT, server_default='')  # 实际地址
    domain = Column(String(100), index=True)  # 主域名
    domain_id = Column(BigInteger, )  # 主域名ID
    city_code = Column(String(50))  # 一级归属地
    region_code = Column(String(100))  # 二级归属地

    ip = Column(String(50), index=True)  # IP地址
    ip_area = Column(String(254), server_default='')  # IP归属地

    title = Column(String(254), server_default='')  # 网站标题
    content = Column(TEXT, server_default='')  # 源码
    web_type = Column(String(30), server_default='', index=True)  # 网站类型
    host_dept = Column(String(254), server_default='')  # 归属单位
    host_type = Column(String(50), server_default='')  # 单位性质

    industries = Column(ARRAY(String), server_default='{}', index=True)  # 行业
    ai_industries = Column(ARRAY(String), server_default='{}', index=True)  # 智能分类行业

    tags = Column(ARRAY(String), server_default='{}')  # 标签
    code_language = Column(String(50), server_default='')  # 编程语言
    http_status = Column(Integer(), server_default='-1', index=True)  # http status
    http_status_list = Column(String(254), server_default='')  # http status list
    category = Column(String(50), server_default='', index=True)  # 类别

    is_auto = Column(Boolean, server_default='0')  # 来源

    def as_dict(self, fields=None):
        detail = {
            "id": self.id,
            "url": self.url,
            "effective_url": self.effective_url,
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
            "category": self.category,
            "is_auto": self.is_auto
        }

        if not fields:
            return detail
        return {attr: detail[attr] for attr in fields if attr in detail}





