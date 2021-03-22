from webargs import fields
from project.api.exceptions.customs import InvalidAPIRequest


def validate_domain_archived_shown_fields(field):
    domain_fields = [
        'id', 'name', 'sponsor', 'sponsor_type', 'icp_number', 'icp_source', 'icp_updated', 'website_count',
        'subdomain_count', 'create_time', 'update_time', 'city_code', 'region_code', 'industries', 'national_level',
        'tags'
    ]
    if field not in domain_fields:
        raise InvalidAPIRequest('无效的字段: {}'.format(field))


def validate_website_archived_shown_fields(field):
    domain_fields = [
        'url', 'domain', 'domain_id', 'city_code', 'region_code', 'ip', 'ip_area', 'title', 'web_type', 'host_dept',
        'host_type', 'industries', 'ai_industries', 'tags', 'code_language', 'http_status', 'http_status_list',
        'category', 'id']

    if field not in domain_fields:
        raise InvalidAPIRequest('无效的字段: {}'.format(field))


update_system_schema = {
    'website_archived_shown_fields': fields.List(fields.Str(validate=validate_website_archived_shown_fields)),
    'domain_archived_shown_fields': fields.List(fields.Str(validate=validate_domain_archived_shown_fields)),
    'domain_recycler_shown_fields': fields.List(fields.Str()),
    'website_recycler_shown_fields': fields.List(fields.Str()),
}


update_service_schema = {
    'ip_server': fields.Str(),
    'icp_server': fields.Str(),
    'subdomain_server': fields.Str(),
    'cache_dispatch': fields.Str(),
    'cache_query': fields.Str(),
    'mail_server': fields.Str(),
    'mail_account': fields.Str(),
    'mail_auth_code': fields.Str(),
    'mail_auth_token': fields.Str(),
    'ai_industry': fields.Str(),
    'cache_callback': fields.Str(),
    'cache_server': fields.Str(),
    'runserver': fields.Str(),
    'search_engine': fields.Str(),
    'brute_server': fields.Str(),
    'fdns_server': fields.Str(),

}
