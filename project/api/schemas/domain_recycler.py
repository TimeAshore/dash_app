from webargs import fields
from project.api.models import DomainRecycler, db
from project.api.schemas import OneOf, length_validator
from project.api.exceptions.customs import RecordNotFound


def domain_id_in_db(domain_id):
    if not db.session.query(DomainRecycler).get(domain_id):
        raise RecordNotFound('无此主域名')


delete_domain_recycler_args = {
    'domain_recycler_ids': fields.List(fields.Int(validate=domain_id_in_db), required=True)
}

restore_domain_recycler_args = {
    'domain_recycler_ids': fields.List(fields.Int(validate=domain_id_in_db), required=True)
}

search_recycler_domains_schema = {
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
        'city_codes': fields.List(fields.Str())
    }, missing={})
}
