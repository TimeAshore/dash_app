from webargs import fields
from project.api.exceptions.customs import InvalidAPIRequest, RecordNotFound, RecordAlreadyExists
from project.api.schemas import OneOf, length_validator


export_schema = {
    'table': fields.Str(required=True),
    "page": fields.Int(missing=-1),  # 默认全部导出
    "size": fields.Int(missing=10, validate=length_validator),
    'order': fields.Nested({
        'field': fields.Str(missing='create_time'),
        'direction': fields.Str(missing='desc', validate=OneOf(['asc', 'desc'], desc="只能是asc和desc两种排序之一"))
    }, missing={}),
    'fields': fields.List(fields.Str()),
    'filter': fields.Str(missing='')
}

# 'filter': fields.Nested({
#         'name': fields.Str(missing=""),
#         'city_codes': fields.List(fields.Str()),
#         'sponsor': fields.Str(missing=""),
#         'sponsor_types': fields.List(fields.Str()),
#         'only_national_level': fields.Boolean(),
#
#         'url': fields.Str(missing=""),
#         'title': fields.Str(missing=""),
#         'domain': fields.Str(missing=""),
#         'host_dept': fields.Str(missing=""),
#         'categories': fields.List(fields.Str()),
#         'region_codes': fields.List(fields.Str()),
#         'http_statuses': fields.List(fields.Str()),
#         'host_types': fields.List(fields.Str()),
#         'web_types': fields.List(fields.Str()),
#         'industries': fields.List(fields.Str()),
#         'not_industries': fields.List(fields.Str()),
#         'tags': fields.List(fields.Str())
#     }, missing={})

