# services/socamas/project/api/bizs/domain_archived_biz.py
from .base import BaseBiz
from .setting_biz import SettingBiz
from ..models import DomainArchived, DomainRecycler


class DomainArchivedBiz(BaseBiz):

    def __init__(self):
        super(DomainArchivedBiz, self).__init__()
        self.model = DomainArchived
        self.allow_query_all = True

    def _build_query_filter(self, query, condition, strict=False):
        if condition.get('name'):
            query = query.filter(self.model.name.ilike('%' + condition['name'] + '%'))
        if condition.get('city_codes'):
            query = query.filter(self.model.city_code.in_(condition['city_codes']))
        if condition.get('sponsor'):
            query = query.filter(self.model.sponsor.like('%' + condition['sponsor'] + '%'))
        if condition.get('sponsor_types'):
            query = query.filter(self.model.sponsor_type.in_(condition['sponsor_types']))
        if condition.get('only_icp') is True:
            query = query.filter(self.model.sponsor.notin_(['未备案', '']))
        if condition.get('no_city') is True:
            query = query.filter(self.model.city_code.is_(None))
        if 'only_national_level' in condition:
            query = query.filter(self.model.national_level.is_(condition['only_national_level']))
        if condition.get('tags'):
            for tag in condition['tags']:
                query = query.filter(self.model.tags.any(tag))
        return query

    def domain_archive_add(self, domain_archive_info):
        name = domain_archive_info.get('name').strip()
        domain_archive = self.session.query(DomainArchived).filter(DomainArchived.name == name).first()
        print(domain_archive_info)
        print(domain_archive_info.get('tags', ''))
        if domain_archive is None:
            domain_archive = DomainArchived(
                name=domain_archive_info.get('name'),
                icp_number=domain_archive_info.get('icp_number', ''),
                icp_source=domain_archive_info.get('icp_source', 'beian.miit.gov.cn'),
                sponsor=domain_archive_info.get('sponsor', ''),
                sponsor_type=domain_archive_info.get('sponsor_type', ''),
                city_code=domain_archive_info.get('city_code', ''),
                region_code=domain_archive_info.get('region_code', ''),
                national_level=domain_archive_info.get('national_level', False),
                tags=domain_archive_info.get('tags', '')

            )
            self.session.add(domain_archive)
            self.safe_commit()
            return domain_archive.as_dict()

    def domain_archive_delete(self, server_info):
        domain_archived_ids = server_info.get('domain_archived_ids')
        for domain_archive_id in domain_archived_ids:
            domain_archive = self.find(id=domain_archive_id)
            self.delete(id=domain_archive_id)
            domain_recycle = DomainRecycler(**domain_archive.as_dict())
            self.session.add(domain_recycle)
        self.safe_commit()

    def domain_archive_update(self, server_info):
        domain_archive = self.find(id=server_info.get('id'))
        for attr in ['icp_number', 'sponsor', 'sponsor_type', 'city_code', 'region_code', 'national_level', 'tags']:
            if server_info.get(attr) is not None:
                setattr(domain_archive, attr, server_info[attr])
        self.safe_commit()
        return domain_archive.as_dict()

    def query_archive_domain(self, server_info):
        query = self.session.query(self.model)
        return self.base_query(query, **server_info)

    def _build_json_data(self, data, filter_count, total_count, fields=None, **kwargs):
        if fields is None:
            setting_biz = SettingBiz()
            fields = setting_biz.get_domain_archived_setting2()['domain_archived_shown_fields']
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

    def get_total_domain(self):
        domains = self.session.query(DomainArchived.name).all()

        return [domain[0] for domain in domains]
