from webargs import fields

single_domain = {
    'domain': fields.Str(required=True)
}


dispatch_domains = {
    'domains': fields.List(fields.Str())
}
