from webargs import fields
from project.api.schemas import OneOf, length_validator
from project.api.exceptions.customs import RecordAlreadyExists, RecordNotFound, InvalidAPIRequest
from project.api.models import WebsiteArchived, db, WebsiteRecycler, WebsiteBanned, WebsiteDuplicated, DomainRecycler, \
    DomainArchived, Industry, City, Region


def website_id_in_db(website_id):
    if not db.session.query(WebsiteArchived).get(website_id):
        raise RecordNotFound('无此网站')


def url_not_in_db(url):
    if db.session.query(WebsiteRecycler).filter_by(url=url).first():
        raise RecordNotFound('网站回收站中已有此网站')
    if db.session.query(WebsiteBanned).filter_by(url=url).first():
        raise RecordNotFound('网站黑名单中已有此网站')
    if db.session.query(WebsiteDuplicated).filter_by(url=url).first():
        raise RecordNotFound('网站重复网站中已有此网站')
    if db.session.query(WebsiteArchived).filter_by(url=url).first():
        raise RecordNotFound('已有此网站')


def domain_in_db(domain):
    if db.session.query(DomainRecycler).filter_by(name=domain).first():
        raise RecordAlreadyExists('此网站主域名已放入回收站')
    if not db.session.query(DomainArchived).filter_by(name=domain).first():
        raise RecordAlreadyExists('请先添加此网站主域名')


def validate_shown_fields(field):
    domain_fields = [
        'url', 'domain', 'domain_id', 'city_code', 'region_code', 'ip', 'ip_area', 'title', 'web_type', 'host_dept',
        'host_type', 'industries', 'ai_industries', 'tags', 'code_language', 'http_status', 'http_status_list',
        'category', 'id']

    if field not in domain_fields:
        raise InvalidAPIRequest('无效的字段: {}'.format(field))


def host_type_in_db(sponsor_type):
    if sponsor_type not in ['个人', '政府机关', '企业', '事业单位', '社会团体', '其他', '民办非企业单位']:
        raise RecordNotFound('无此单位性质')


def industry_in_db(industry):
    if not db.session.query(Industry).filter_by(name=industry).first():
        raise RecordNotFound('无此行业: {}'.format(industry))


def city_code_in_db(code):
    if not db.session.query(City).filter_by(name=code).first():
        raise RecordNotFound('无此一级归属地')


def region_code_in_db(code):
    if not db.session.query(Region).filter_by(name=code).first():
        raise RecordNotFound('无此二级归属地')


def catagory_in_db(catagory):
    if catagory not in ['高等院校', '上市公司']:
        raise RecordNotFound('无此类别')


def tag_in_db(catagory):
    if catagory not in ['高等院校', '医院', '关键信息基础设施']:
        raise RecordNotFound('无此标签:{}'.format(catagory))


def status_in_db(status):
    codes = [6, 7, 28, 52, 56, 200, 301, 302, 303, 307, 400, 401, 403, 404, 500, 501, 502, 503, 504, 520, 521, 523, 530]
    if status not in codes:
        raise RecordNotFound('HTTP状态码无效')


add_website_archived_args = {
    'url': fields.Str(required=True, validate=url_not_in_db),
    'title': fields.Str(required=True),
    'domain': fields.Str(required=True, validate=domain_in_db),
    'ip': fields.Str(),
    'ip_area': fields.Str(),
    'host_dept': fields.Str(),
    'host_type': fields.Str(validate=host_type_in_db),
    'industries': fields.List(fields.Str(validate=industry_in_db)),
    'city_code': fields.Str(validate=city_code_in_db),
    'region_code': fields.Str(validate=region_code_in_db),
    'category': fields.Str(validate=catagory_in_db),
    'http_status': fields.Int(validate=status_in_db),
    'tags': fields.List(fields.Str(validate=tag_in_db)),
    'web_type': fields.Str(validate=OneOf(['web', 'system']))
}

update_website_archived_args = {
    'id': fields.Int(required=True, validate=website_id_in_db),
    'domain': fields.Str(validate=domain_in_db),
    'url': fields.Str(validate=url_not_in_db),
    'host_dept': fields.Str(),
    'host_type': fields.Str(validate=host_type_in_db),
    'city_code': fields.Str(validate=city_code_in_db),
    'region_code': fields.Str(validate=region_code_in_db),
    'ip': fields.Str(),
    'ip_area': fields.Str(),
    'category': fields.Str(validate=catagory_in_db),
    'http_status': fields.Int(validate=status_in_db),
    'title': fields.Str(),
    'industries': fields.List(fields.Str(validate=industry_in_db)),
    'tags': fields.List(fields.Str(validate=tag_in_db)),
    'web_type': fields.Str(validate=OneOf(['web', 'system']))
}

query_website_archived_args = {
    'page': fields.Int(missing=0),
    'size': fields.Int(missing=15, validate=length_validator),
    'order': fields.Nested({
        'field': fields.Str(missing='create_time'),
        'direction': fields.Str(missing='desc', validate=OneOf(['asc', 'desc']))
    }, missing={}),
    'fields': fields.List(fields.Str()),
    'filter': fields.Nested({
        'url': fields.Str(),
        'title': fields.Str(),
        'domain': fields.Str(),
        'host_dept': fields.Str(),
        'categories': fields.List(fields.Str()),
        'city_codes': fields.List(fields.Str()),
        'region_codes': fields.List(fields.Str()),
        'industries': fields.List(fields.Str()),
        'not_industries': fields.List(fields.Str()),
        'host_types': fields.List(fields.Str()),
        'http_statuses': fields.List(fields.Int()),
        'web_types': fields.List(fields.Str()),
        'tags': fields.List(fields.Str())
    }, missing={})
}

delete_website_archived_args = {
    'website_archived_ids': fields.List(fields.Int(validate=website_id_in_db), required=True)
}

update_shown_fields_schema = {
    'website_archived_shown_fields': fields.List(fields.Str(validate=validate_shown_fields), required=True)
}
