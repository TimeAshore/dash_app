from flask import Blueprint, jsonify
from webargs.flaskparser import use_args

from project.api.bizs import IndustryBiz
from project.api.schemas.industry import add_industry


info_blueprint = Blueprint("info", __name__, url_prefix='/info')
payload_location = ('json', )


@info_blueprint.route('/industry/list', methods=['GET'])
def get_industries():

    industry_biz = IndustryBiz()
    data = industry_biz._query()
    return jsonify({
        'status': True,
        'data': data
    }), 200


@info_blueprint.route('/industry/add', methods=['POST'])
@use_args(add_industry, locations=payload_location)
def add_industry(payload):

    industry_biz = IndustryBiz()
    data = industry_biz.add(**payload)
    return jsonify({
        'status': True,
        'data': data,
    }), 201


@info_blueprint.route('/status/list', methods=['GET'])
def get_statuses():

    codes = [6, 7, 28, 52, 56, 200, 301, 302, 303, 307, 400, 401, 403, 404, 500, 501, 502, 503, 504, 520, 521, 523, 530]
    return jsonify({
        'status': True,
        'data': codes
    }), 200


@info_blueprint.route('/website/tags/list', methods=['GET'])
def get_website_tags():

    tags = ['关键信息基础设施']
    return jsonify({
        'status': True,
        'data': tags
    }), 200
