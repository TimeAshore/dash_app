from flask import Blueprint, jsonify
from webargs.flaskparser import use_args

from project.api.bizs import WebsiteRecyclerBiz
from project.api.schemas.website_recycler import query_recycler_schema, delete_website_recycler_args, restore_website_recycler_args


website_recycler_blueprint = Blueprint('website_recycler', __name__, url_prefix='/website/recycler')
payload_location = ('json',)


@website_recycler_blueprint.route('/list', methods=['POST'])
@use_args(query_recycler_schema, locations=payload_location)
def query_recycler(payload):

    website_recycler_biz = WebsiteRecyclerBiz()
    data = website_recycler_biz._query(**payload)
    return jsonify({
        'status': True,
        'data': data
    }), 201


@website_recycler_blueprint.route('/delete', methods=['POST'])
@use_args(delete_website_recycler_args, locations=payload_location)
def delete_recycler(payload):

    website_recycler_biz = WebsiteRecyclerBiz()
    website_recycler_biz._delete(payload)
    return jsonify({
        'status': True
    }), 204


@website_recycler_blueprint.route('/restore', methods=['POST'])
@use_args(restore_website_recycler_args, locations=payload_location)
def restore_recycler(payload):

    website_recycler_biz = WebsiteRecyclerBiz()
    website_recycler_biz._restore(payload)
    return jsonify({
        'status': True
    }), 200

