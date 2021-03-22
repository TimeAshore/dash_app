from flask import Blueprint, jsonify
from webargs.flaskparser import use_args
from project.api.schemas.domain_recycler import delete_domain_recycler_args, restore_domain_recycler_args, search_recycler_domains_schema
from project.api.bizs.domain_recycler_biz import DomainRecyclerBiz


domain_recycler_blueprint = Blueprint('domain_recycler', __name__, url_prefix='/domain/recycler')
payload_location = ('json',)


@domain_recycler_blueprint.route('/delete', methods=['POST'])
@use_args(delete_domain_recycler_args, locations=payload_location)
def delete_domain_recycler(args):
    domain_recycler_business = DomainRecyclerBiz()
    domain_recycler_business.domain_recycler_delete(args)
    return jsonify({
        "status": True
    }), 201


@domain_recycler_blueprint.route('/restore', methods=['POST'])
@use_args(restore_domain_recycler_args, locations=payload_location)
def restore_domain_recycler(args):
    domain_recycler_business = DomainRecyclerBiz()
    domain_recycler_business.domain_recycler_restore(args)
    return jsonify({
        "status": True
    }), 201


@domain_recycler_blueprint.route('/list', methods=['POST'])
@use_args(search_recycler_domains_schema, locations=payload_location)
def search_domain_recycler(args):
    domain_recycler_business = DomainRecyclerBiz()
    data = domain_recycler_business.query_archive_recycler(args)
    return jsonify({
        "status": True, "data": data
    }), 200
