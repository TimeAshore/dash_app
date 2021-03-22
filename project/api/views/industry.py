from flask import Blueprint, jsonify
from webargs.flaskparser import use_args

from project.api.bizs import IndustryBiz
from project.api.schemas.industry import add_industry


industry_blueprint = Blueprint("industry", __name__, url_prefix='/industry')
payload_location = ('json', )


@industry_blueprint.route('/list', methods=['GET'])
def get_industries():

    industry_biz = IndustryBiz()
    data = industry_biz._query()
    return jsonify({
        'status': True,
        'data': data
    }), 200


@industry_blueprint.route('/add', methods=['POST'])
@use_args(add_industry, locations=payload_location)
def add_industry(payload):

    industry_biz = IndustryBiz()
    data = industry_biz.add(**payload)
    return jsonify({
        'status': True,
        'data': data,
    }), 201

