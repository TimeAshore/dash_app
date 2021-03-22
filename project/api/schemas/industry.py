from webargs import fields


add_industry = {
    'name': fields.Str(required=True),
    'spell': fields.Str(),
    'website_count': fields.Integer()
}


