from webargs import fields

from project.api.models import db
from project.api.models import WebsiteRecycler
from project.api.exceptions.param import ParamException


class OneOf:
    def __init__(self, choices, desc=''):
        self.choices = choices
        self.desc = desc

    def __call__(self, value):
        if value not in self.choices:
            raise Exception(self.desc)


def length_validator(length):
    if length < 0 or length > 100:
        raise Exception('参数错误')


def website_id_in_db(website_id):
    if not db.session.query(WebsiteRecycler).get(website_id):
        raise ParamException('无此主域名')


query_recycler_schema = {
    'start': fields.Int(missing=0),
    'length': fields.Int(missing=15, validate=length_validator),
    'order': fields.Nested({
        'field': fields.Str(missing='create_time'),
        'direction': fields.Str(missing='desc', validate=OneOf(['asc', 'desc']))
    }, missing={}),
    'fields': fields.List(fields.Str()),
    'filter': fields.Nested({
        'url': fields.Str(missing=""),
        'title': fields.Str(missing=""),
        'domain': fields.Str(missing=""),
        'host_dept': fields.Str(missing="")
    }, missing={})
}


delete_website_recycler_args = {
    'website_recycler_ids': fields.List(fields.Int(validate=website_id_in_db), required=True)
}

restore_website_recycler_args = {
    'website_recycler_ids': fields.List(fields.Int(validate=website_id_in_db), required=True)
}
