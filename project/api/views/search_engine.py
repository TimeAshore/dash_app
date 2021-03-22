from flask import Blueprint, jsonify
from webargs.flaskparser import use_args

from project.api.bizs import SearchEngineBiz
from project.api.schemas.search_engine import dispatch_domains, single_domain

search_engine_blueprint = Blueprint('search_engine', __name__, url_prefix='/search_engine')
payload_location = ('json',)


@search_engine_blueprint.route('/single', methods=['POST'])
@use_args(single_domain, locations=payload_location)
def single_dispatch(payload):
    search_engine_biz = SearchEngineBiz()
    data = search_engine_biz.single_dispatch(payload['domain'])
    return jsonify({
        'status': True,
        'data': data
    }), 201


@search_engine_blueprint.route('/generater', methods=['POST'])
def get_subdomain():
    """search_engine全量返回"""
    search_engine_biz = SearchEngineBiz()
    data = search_engine_biz.get_subdomain()
    return jsonify({
        'status': True,
        'data': data
    }), 201


@search_engine_blueprint.route('/dispatch', methods=['POST'])
@use_args(dispatch_domains, locations=payload_location)
def dispatch(payload):
    search_engine_biz = SearchEngineBiz()
    data = search_engine_biz.dispatch(payload.get('domains', []))
    return jsonify({
        'status': True,
        'data': data
    }), 201
