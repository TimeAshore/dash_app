from sqlalchemy import or_

from .base import BaseBiz
from .setting_biz import SettingBiz
from project.api.models import WebsiteArchived, DomainArchived, WebsiteRecycler


class WebsiteArchivedBiz(BaseBiz):

    def __init__(self):
        super(WebsiteArchivedBiz, self).__init__()
        self.model = WebsiteArchived
        self.allow_query_all = True

    @property
    def fields(self):
        return ['url', 'domain', 'domain_id', 'city_code', 'region_code', 'ip', 'ip_area', 'title', 'web_type',
                                                                                                    'host_dept',
                'host_type', 'industries', 'ai_industries', 'tags', 'code_language', 'http_status', 'http_status_list',
                'category']

    def _build_query_filter(self, query, condition, strict=False):
        for attr in ['url', 'title', 'domain', 'host_dept']:
            if condition.get(attr):
                cls_attr = getattr(self.model, attr)
                query = query.filter(cls_attr.ilike('%' + condition[attr] + '%'))

        if condition.get('categories'):
            query = query.filter(self.model.category.in_(condition['categories']))
        if condition.get('city_codes'):
            query = query.filter(self.model.city_code.in_(condition['city_codes']))
        if condition.get('region_codes'):
            query = query.filter(self.model.region_code.in_(condition['region_codes']))
        if condition.get('http_statuses'):
            query = query.filter(self.model.http_status.in_(condition['http_statuses']))
        if condition.get('host_types'):
            query = query.filter(self.model.host_type.in_(condition['host_types']))
        if condition.get('web_types'):
            query = query.filter(self.model.web_type.in_(condition['web_types']))
        if condition.get('industries'):
            # Include industries
            # For example: select url from table where industry in ('{edu}', '{gov}', '{edu,gov}', 'edu,medic'...)
            industries = []
            for industrie in condition['industries']:
                all_industrie = self.session.query(WebsiteArchived.industries).filter(
                    or_(WebsiteArchived.industries[1].like(f'%{industrie}%'),
                        WebsiteArchived.industries[2].like(f'%{industrie}%'),
                        WebsiteArchived.industries[3].like(f'%{industrie}%'),
                        WebsiteArchived.industries[4].like(f'%{industrie}%'))
                ).group_by(WebsiteArchived.industries).all()
                for industrie in all_industrie:
                    start = industrie[0][0]
                    for eve in industrie[0][1:]:
                        start = start + f',{eve}'
                    industries.append('{' + start + '}')
            query = query.filter(self.model.industries.in_(industries))
        if condition.get('not_industries'):
            # Get rid of industries
            # For example: select url from table where industry not in ('{edu}', '{gov}', '{edu,gov}', 'edu,medic'...)
            forbidden_indus = []
            for industrie in condition['not_industries']:
                all_industrie = self.session.query(WebsiteArchived.industries).filter(
                    or_(WebsiteArchived.industries[1].like(f'%{industrie}%'),
                        WebsiteArchived.industries[2].like(f'%{industrie}%'),
                        WebsiteArchived.industries[3].like(f'%{industrie}%'),
                        WebsiteArchived.industries[4].like(f'%{industrie}%'))
                ).group_by(WebsiteArchived.industries).all()
                for industrie in all_industrie:
                    start = industrie[0][0]
                    for eve in industrie[0][1:]:
                        start = start + f',{eve}'
                    forbidden_indus.append('{' + start + '}')
            query = query.filter(self.model.industries.notin_(forbidden_indus))
        if condition.get('tags'):
            for tag in condition['tags']:
                query = query.filter(self.model.tags.any(tag))

        return query

    def website_archive_add(self, website_archive_info):
        if 'domain_id' not in website_archive_info.keys():
            domain = self.session.query(DomainArchived).filter_by(name=website_archive_info['domain']).first()
            website_archive_info.update({'domain_id': domain.id})
        website_archived = WebsiteArchived(**website_archive_info)
        self.session.add(website_archived)
        self.safe_commit()
        return website_archived.as_dict()

    def website_archive_update(self, website_archive_info):
        website_archive = self.find(id=website_archive_info.get('id'))
        for attr in ['url', 'domain', 'host_dept', 'host_type', 'industries', 'tags',
                     'city_code', 'region_code', 'web_type', 'ip', 'ip_area', 'title', 'category',
                     'http_status']:
            if website_archive_info.get(attr) is not None:
                setattr(website_archive, attr, website_archive_info[attr])
        self.safe_commit()
        return website_archive.as_dict()

    def website_archive_delete(self, server_info):
        website_archived_ids = server_info.get('website_archived_ids')
        for website_archive_id in website_archived_ids:
            website_archive = self.find(id=website_archive_id)
            self.delete(id=website_archive_id)
            website_recycle = WebsiteRecycler(**website_archive.as_dict())
            self.session.add(website_recycle)
        self.safe_commit()

    def query_archive_website(self, server_info):
        query = self.session.query(self.model)
        return self.base_query(query, **server_info)

    def _build_json_data(self, data, filter_count, total_count, fields=None, **kwargs):
        if fields is None:
            setting_biz = SettingBiz()
            fields = setting_biz.get_website_archived_setting2()['website_archived_shown_fields']
        return {
            "records": [self.trans2dict(obj, fields=fields, **kwargs) for obj in data],
            "total_count": total_count,
            "filter_count": filter_count
        }

    def _build_query_order(self, query, order):
        order_field, order_dir = order.get('field', 'update_time'), order.get('direction', 'desc')
        if order_field == 'city':
            order_field = 'city_code'
        if order_field == 'region':
            order_field = 'region_code'
        if order_field not in self.fields:
            order_field = 'update_time'
        obj_attr = getattr(self.model, order_field)
        return query.order_by(getattr(obj_attr, order_dir)()).order_by(self.model.id.desc())
