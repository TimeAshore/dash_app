from webargs import fields
from project.api.schemas import OneOf, length_validator
from project.api.models import DomainArchived, db, City, Region, DomainRecycler
from project.api.exceptions.customs import RecordAlreadyExists, RecordNotFound, InvalidAPIRequest


def domain_id_in_db(domain_id):
    if not db.session.query(DomainArchived).get(domain_id):
        raise RecordNotFound('无此主域名')


def validate_shown_fields(field):
    domain_fields = [
        'id', 'name', 'sponsor', 'sponsor_type', 'icp_number', 'icp_source', 'icp_updated', 'website_count',
        'subdomain_count', 'create_time', 'update_time', 'city_code', 'region_code', 'industries', 'national_level',
        'tags'
    ]
    if field not in domain_fields:
        raise InvalidAPIRequest('无效的字段: {}'.format(field))


def domain_not_in_db(domain):
    if db.session.query(DomainRecycler).filter_by(name=domain).first():
        raise RecordAlreadyExists('此主域名已放入回收站')
    if db.session.query(DomainArchived).filter_by(name=domain).first():
        raise RecordAlreadyExists('已有此主域名')


def sponsor_type_in_db(sponsor_type):
    if sponsor_type not in ['个人', '政府机关', '企业', '事业单位', '社会团体', '其他', '民办非企业单位']:
        raise RecordNotFound('无此单位性质')


def tags_in_db(sponsor_type):
    if sponsor_type not in ['医院', '上市单位']:
        raise RecordNotFound('无此标签')


def city_code_in_db(code):
    if not db.session.query(City).filter_by(name=code).first():
        raise RecordNotFound('无此一级归属地')


def region_code_in_db(code):
    if not db.session.query(Region).filter_by(name=code).first():
        raise RecordNotFound('无此二级归属地')


add_domain_archived_args = {

    'name': fields.Str(required=True, validate=domain_not_in_db),
    'city_code': fields.Str(missing="", validate=city_code_in_db),
    'region_code': fields.Str(missing="", validate=region_code_in_db),
    'icp_number': fields.Str(missing=""),
    'national_level': fields.Boolean(missing=False),
    'icp_source': fields.Str(missing="beian.miit.gov.cn"),
    'sponsor': fields.Str(missing=""),
    'sponsor_type': fields.Str(missing="", validate=sponsor_type_in_db),
    'tags': fields.List(fields.Str(validate=tags_in_db)),
}


delete_domain_archived_args = {
    'domain_archived_ids': fields.List(fields.Int(validate=domain_id_in_db), required=True)
}


update_domain_archived_args = {
    'id': fields.Int(required=True, validate=domain_id_in_db),
    'sponsor': fields.Str(),
    'sponsor_type': fields.Str(validate=sponsor_type_in_db),
    'icp_number': fields.Str(),
    'city_code': fields.Str(validate=city_code_in_db),
    'region_code': fields.Str(validate=region_code_in_db),
    'national_level': fields.Bool(),
    'tags': fields.List(fields.Str(validate=tags_in_db)),
}


update_shown_fields_schema = {
    'domain_archived_shown_fields': fields.List(fields.Str(validate=validate_shown_fields), required=True)
}

query_domain_archived_args = {
    'page': fields.Int(missing=0),
    'size': fields.Int(missing=15, validate=length_validator),
    'order': fields.Nested({
        'field': fields.Str(missing='create_time'),
        'direction': fields.Str(missing='desc', validate=OneOf(['asc', 'desc'], desc="只能是asc和desc两种排序之一"))
    }, missing={}),
    'fields': fields.List(fields.Str()),
    'filter': fields.Nested({
        'name': fields.Str(missing=""),
        'sponsor': fields.Str(missing=""),
        'sponsor_types': fields.List(fields.Str()),
        'tags': fields.List(fields.Str()),
        'city_codes': fields.List(fields.Str()),
        'only_icp': fields.Boolean(),
        'only_national_level': fields.Boolean(),
        'no_city': fields.Boolean()
    }, missing={})
}
