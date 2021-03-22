from flask import Blueprint, jsonify
from webargs.flaskparser import use_args

from project.api.bizs import RegionBiz
from project.api.schemas.region import region_schema

region_blueprint = Blueprint('region', __name__)
payload_location = ('json',)


@region_blueprint.route('/region/list', methods=['POST'])
@use_args(region_schema, locations=payload_location)
def obtain_city(payload):

    region_biz = RegionBiz()
    data = region_biz._query(**payload)
    return jsonify({
        'status': True,
        "data": data,
    }), 201

