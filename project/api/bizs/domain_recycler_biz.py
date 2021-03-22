# services/socamas/project/api/bizs/domain_recycler_biz.py
from .base import BaseBiz
from ..models import DomainRecycler, DomainArchived
from .setting_biz import SettingBiz


class DomainRecyclerBiz(BaseBiz):

    def __init__(self):
        super(DomainRecyclerBiz, self).__init__()
        self.model = DomainRecycler
        self.allow_query_all = True

    @property
    def fields(self):
        return ['domain', 'sponsor', 'sponsor_type',
                'icp_number', 'icp_updated',
                'city_code', 'region_code',
                'website_count', 'subdomain_count']

    def domain_recycler_delete(self, server_info):
        domain_recycler_ids = server_info.get('domain_recycler_ids')
        for domain_recycler_id in domain_recycler_ids:
            self.delete(id=domain_recycler_id)
        self.safe_commit()

    def domain_recycler_restore(self, server_info):
        domain_recycler_ids = server_info.get('domain_recycler_ids')
        for domain_recycler_id in domain_recycler_ids:
            domain_recycler = self.find(id=domain_recycler_id)
            self.delete(id=domain_recycler_id)
            domain_archived = DomainArchived(**domain_recycler.as_dict())
            self.session.add(domain_archived)
        self.safe_commit()

    def _build_query_filter(self, query, condition, strict=False):
        if condition.get('name'):
            query = query.filter(self.model.name.like('%' + condition['name'] + '%'))
        if condition.get('sponsor'):
            query = query.filter(self.model.sponsor.like('%' + condition['sponsor'] + '%'))
        if condition.get('city_codes'):
            query = query.filter(self.model.city_code.in_(condition['city_codes']))
        return query

    def _build_json_data(self, data, filter_count, total_count, fields=None, **kwargs):
        if fields is None:
            setting_biz = SettingBiz()
            fields = setting_biz.get_domain_recycler_setting()['domain_recycler_shown_fields']
        return {
            "records": [self.trans2dict(obj, fields=fields, **kwargs) for obj in data],
            "total_count": total_count,
            "filter_count": filter_count
        }

    def query_archive_recycler(self, server_info):
        query = self.session.query(self.model)
        return self.base_query(query, **server_info)
