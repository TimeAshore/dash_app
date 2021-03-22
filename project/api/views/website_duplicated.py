from flask import Blueprint, jsonify
from webargs.flaskparser import use_args

from project.api.bizs.website_duplicated_biz import WebsiteDuplicatedBiz
from project.api.schemas.website_duplicated import delete_args, restore_args, query_args

website_duplicated_blueprint = Blueprint('website_duplicated', __name__)
payload_location = ('json',)


@website_duplicated_blueprint.route('/website/duplicated/delete', methods=['DELETE'])
@use_args(delete_args, locations=payload_location)
def delete(payload):
    """
    删除
    :param payload:
    :return:
    """
    website_ban = WebsiteDuplicatedBiz()
    website_ban.delete(payload)

    return jsonify({
        'status': True
    }), 204


@website_duplicated_blueprint.route('/website/duplicated/restore', methods=['POST'])
@use_args(restore_args, locations=payload_location)
def restore(payload):
    """
    还原
    :param payload:
    :return:
    """
    website_ban = WebsiteDuplicatedBiz()
    website_ban.restore(payload)

    return jsonify({
        'status': True
    }), 201


@website_duplicated_blueprint.route('/website/duplicated/query', methods=['POST'])
@use_args(query_args, locations=payload_location)
def query(payload):
    """
    查询
    :param payload:
    :return:
    """
    website_ban_biz = WebsiteDuplicatedBiz()
    data = website_ban_biz._query(payload)

    return jsonify({
        'data': data,
        'status': True
    }), 201




