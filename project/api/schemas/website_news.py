from tld import get_fld
from webargs import fields

from project.api.schemas import OneOf, length_validator
from project.api.exceptions.customs import InvalidAPIRequest, RecordAlreadyExists, RecordNotFound
from project.api.models import db, DomainArchived, WebsiteArchived, WebsiteRecycler, WebsiteNews, WebsiteBanned, WebsiteDuplicated


def website_url_not_in_db(url):
    domain = db.session.query(DomainArchived).filter_by(name=get_fld(url)).first()
    if not domain:
        raise InvalidAPIRequest('主域名未收录，请先添加主域名')
    for model in [WebsiteArchived, WebsiteNews, WebsiteRecycler, WebsiteBanned, WebsiteDuplicated]:
        if db.session.query(model).filter_by(url=url.strip('/')).first():
            raise RecordAlreadyExists('已有此网站')


def id_in_db(id):
    if not db.session.query(WebsiteNews).filter_by(id=id).first():
        raise RecordNotFound('无此数据')


query_args = {
    'page': fields.Int(missing=0),
    'size': fields.Int(missing=25, validate=length_validator),
    'order': fields.Nested({
        'field': fields.Str(missing='create_time'),
        'direction': fields.Str(missing='desc', validate=OneOf(['asc', 'desc']))
    }, missing={}),
    'fields': fields.List(fields.Str()),
    'filter': fields.Nested({
        'url': fields.Str(),
        'domain': fields.Str(),
        'ip_area': fields.Str(),
        'title': fields.Str(),
        'http_status': fields.Str()
    }, missing={})
}


add_args = {
    'url': fields.Str(validate=website_url_not_in_db, required=True)
}


filter_args = {
    'condition': fields.Str()
}

mend_args = {
    'condition': fields.Str()
}

archived_args = {
    'ids': fields.List(fields.Int(validate=id_in_db), required=True)
}

update_args = {
    'id': fields.Int(validate=id_in_db, required=True),
    'title': fields.Str(),
    'city_code': fields.Str(),
    'region_code': fields.Str(),
    'host_dept': fields.Str(),
    'host_type': fields.Str(),
    'web_type': fields.Str(),
    'industries': fields.List(fields.Str()),
    'tags': fields.List(fields.Str()),
    'category': fields.Str()
}

ban_args = {
    'ids': fields.List(fields.Int(validate=id_in_db), required=True),
    'group': fields.Str()
}

delete_args = {
    'ids': fields.List(fields.Int(validate=id_in_db), required=True)
}

