from flask import Blueprint, jsonify
from webargs.flaskparser import use_args

from project.api.bizs.website_banned_biz import WebsiteBannedBiz
from project.api.schemas.website_banned import delete_args, restore_args, query_args

website_banned_blueprint = Blueprint('website_banned', __name__)
payload_location = ('json',)


@website_banned_blueprint.route('/website/ban/delete', methods=['DELETE'])
@use_args(delete_args, locations=payload_location)
def delete(payload):
    """
    删除
    :param payload:
    :return:
    """
    website_ban = WebsiteBannedBiz()
    website_ban.delete(payload)

    return jsonify({
        "status": True
    }), 204


@website_banned_blueprint.route('/website/ban/restore', methods=['POST'])
@use_args(restore_args, locations=payload_location)
def restore(payload):
    """
    还原
    :param payload:
    :return:
    """
    website_ban = WebsiteBannedBiz()
    website_ban.restore(payload)

    return jsonify({
        'status': True
    }), 201


@website_banned_blueprint.route('/website/ban/query', methods=['POST'])
@use_args(query_args, locations=payload_location)
def query(payload):
    """
    查询
    :param payload:
    :return:
    """
    website_ban_biz = WebsiteBannedBiz()
    data = website_ban_biz._query(payload)

    return jsonify({
        'data': data,
        'status': True
    }), 201




