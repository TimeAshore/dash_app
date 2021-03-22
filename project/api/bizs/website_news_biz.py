import requests
from tld import get_fld
from sqlalchemy import cast, String

from .base import BaseBiz
from .domain_archived_biz import DomainArchivedBiz
from .website_archived_biz import WebsiteArchivedBiz

from project.api.models import WebsiteNews, DomainArchived, WebsiteBanned


class WebsiteNewsBiz(BaseBiz):

    def __init__(self):
        super(WebsiteNewsBiz, self).__init__()
        self.model = WebsiteNews
        self.allow_query_all = True

    @property
    def fields(self):
        return ['url', 'domain', 'domain_id', 'city_code', 'region_code', 'ip', 'ip_area', 'title', 'web_type'
                                                                                                    'host_dept',
                'host_type', 'industries', 'ai_industries', 'tags', 'code_language', 'http_status', 'http_status_list',
                'category', 'source']

    def _build_query_filter(self, query, condition, strict=False):
        for attr in ['url', 'title', 'http_status', 'host_dept']:
            if condition.get(attr):
                cls_attr = getattr(self.model, attr)
                query = query.filter(cls_attr.ilike('%' + condition[attr] + '%'))
        if condition.get('ip_area'):
            query = query.filter(cast(self.model.ip, String).like('%' + condition['ip_area'] + '%'))
        if condition.get('domain'):
            query = query.filter_by(domain=condition['domain'])
        return query

    @staticmethod
    def get_brute_subs():
        domain_biz = DomainArchivedBiz()
        domains = {
            "domains": domain_biz.get_total_domain()
        }
        response = requests.post(url='http://192.168.199.221/api/socweb/subs', json=domains)
        subs = response.json()['data']
        print(len(subs))
        return subs

    def add(self, url):
        """
        添加新发现
        :param url:
        :return:
        """
        domain = self.session.query(DomainArchived).filter_by(name=get_fld(url)).first()
        website = WebsiteNews(url=url)
        website.domain = domain.name
        website.domain_id = domain.id
        self.session.add(website)
        self.safe_commit()

    def archived(self, payload):
        """
        霹雳帮归档
        :param payload:
        :return:
        """
        for id in payload.get('ids', []):
            website = self.session.query(WebsiteNews).filter_by(id=id).first()

            info = {
                'url': website.url,
                'title': website.title,
                'domain': website.domain,
                'domain_id': website.domain_id,
                'ip': website.ip,
                'ip_area': website.ip_area,
                'host_dept': website.host_dept,
                'host_type': website.host_type,
                'industries': website.industries,
                'city_code': website.city_code,
                'region_code': website.region_code,
                'category': website.category if website.category else '',
                'http_status': website.http_status,
                'tags': website.tags,
                'web_type': website.web_type
            }
            # print("info:", info)

            # 加到archived
            website_archive_biz = WebsiteArchivedBiz()
            website_archive_biz.website_archive_add(info)

            # 从news删除
            self.session.delete(website)
            self.safe_commit()

    def update(self, payload):
        """
        修改
        :param payload:
        :return:
        """
        website = self.session.query(WebsiteNews).filter_by(id=payload.get('id')).first()
        for attr in ['title', 'city_code', 'region_code', 'host_dept', 'host_type', 'web_type', 'industries', 'tags', 'category']:
            if payload.get(attr) is not None:
                setattr(website, attr, payload[attr])

        self.safe_commit()

    def ban(self, payload):
        """
        批量拉黑
        :param payload:
        :return:
        """
        for id in payload.get('ids', []):
            website = self.session.query(WebsiteNews).filter_by(id=id).first()
            banned_website = WebsiteBanned(is_auto=False, group=payload.get('group'), **website.as_dict())
            self.session.add(banned_website)

            self.session.delete(website)
            self.safe_commit()

    def delete(self, payload):
        """
        批量删除
        :param payload:
        :return:
        """
        for id in payload.get('ids', []):
            website = self.session.query(WebsiteNews).filter_by(id=id).first()
            self.session.delete(website)
            self.safe_commit()

    def clear(self):
        """
        清空
        :return:
        """
        self.session.query(WebsiteNews).delete()
        self.safe_commit()

