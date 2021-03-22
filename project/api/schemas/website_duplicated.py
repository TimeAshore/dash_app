from webargs import fields

from project.api.models import db, WebsiteDuplicated
from project.api.schemas import OneOf, length_validator
from project.api.exceptions.customs import RecordNotFound


def id_in_db(id):
    if not db.session.query(WebsiteDuplicated).filter_by(id=id).first():
        raise RecordNotFound('无此数据')


delete_args = {
    'ids': fields.List(fields.Int(validate=id_in_db), required=True)
}

restore_args = {
    'ids': fields.List(fields.Int(validate=id_in_db), required=True)
}

query_args = {
    'page': fields.Int(missing=0),
    'size': fields.Int(missing=25, validate=length_validator),
    'order': fields.Nested({
        'field': fields.Str(missing='create_time'),
        'direction': fields.Str(missing='desc', validate=OneOf(['asc', 'desc']))
    }, missing={}),
    'filter': fields.Nested({
        'url': fields.Str(),
        'title': fields.Str(),
        'effective_url': fields.Str()
    }, missing={})
}
