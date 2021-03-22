from flask import Blueprint, jsonify
from webargs.flaskparser import use_args

from project.api.bizs import RegionBiz
from project.api.schemas.unit import unit_schema

unit_blueprint = Blueprint('unit', __name__)
payload_location = ('json',)


# @unit_blueprint.route('/unit/add', methods=['POST'])
# @use_args(unit_schema, locations=payload_location)
# def obtain_city(payload):
#
#     region_biz = RegionBiz()
#     data = region_biz._query(**payload)
#     return jsonify({
#         'status': True,
#         "data": data,
#     }), 201

