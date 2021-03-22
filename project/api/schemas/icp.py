from webargs import fields


query_icp_schema = {
    'domain': fields.Str(required=True),
    'captcha': fields.Str(),
    'token': fields.Str()
}
