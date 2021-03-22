from flask import Blueprint, jsonify

from project.api.bizs import CityBiz

city_blueprint = Blueprint('city', __name__)
payload_location = ('json',)


@city_blueprint.route('/city/list', methods=['GET'])
def obtain_city():
    print('get')

    city_biz = CityBiz()
    data = city_biz._query()
    return jsonify({
        'status': True,
        "data": data,
    }), 200


