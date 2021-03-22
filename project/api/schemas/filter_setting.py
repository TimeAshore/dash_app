from webargs import fields

from project.api.models import db, BanKeyword, BanGroup
from project.api.schemas import OneOf, length_validator
from project.api.exceptions.customs import RecordNotFound, RecordAlreadyExists


def id_in_db(id):
    if not db.session.query(BanKeyword).filter_by(id=id).first():
        raise RecordNotFound('无此记录')


def id_in_groups(id):
    if not db.session.query(BanGroup).filter_by(id=id).first():
        raise RecordNotFound('无此分组')


def keyword_not_in_db(keyword):
    if db.session.query(BanKeyword).filter_by(keyword=keyword).first():
        raise RecordAlreadyExists(f'已有此关键词: {keyword}')


def name_not_in_db(name):
    if db.session.query(BanGroup).filter_by(name=name).first():
        raise RecordAlreadyExists(f'已有此分组: {name}')


query_args = {
    'page': fields.Int(missing=-1),
    'size': fields.Int(missing=25, validate=length_validator),
    'order': fields.Nested({
        'field': fields.Str(missing='create_time'),
        'direction': fields.Str(missing='desc', validate=OneOf(['asc', 'desc']))
    }, missing={}),
    'filter': fields.Nested({
        'keyword': fields.Str(),
        'typs': fields.List(fields.Str()),
        'groups': fields.List(fields.Str())
    }, missing={})
}

delete_args = {
    'ids': fields.List(fields.Int(validate=id_in_db), required=True)
}

add_args = {
    'keyword': fields.Str(validate=keyword_not_in_db),
    'typ': fields.Str(),
    'group': fields.Str()
}

delete_group_args = {
    'id': fields.Int(validate=id_in_groups, required=True)
}

add_group_args = {
    'name': fields.Str(validate=name_not_in_db, required=True)
}
