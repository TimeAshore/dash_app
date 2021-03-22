from flask import Blueprint, jsonify
from webargs.flaskparser import use_args

from project.api.bizs import IcpBiz
from project.api.schemas.icp import query_icp_schema

icp_blueprint = Blueprint('icp', __name__)
payload_location = ('json',)


@icp_blueprint.route('/icp/captcha', methods=['GET'])
def get_icp_captcha():
    icp_biz = IcpBiz()
    data = icp_biz.get_captcha()
    return jsonify({
        'status': True,
        'data': data
    }), 200


@icp_blueprint.route('/icp/query', methods=['POST'])
@use_args(query_icp_schema, locations=payload_location)
def query_icp(payload):
    """查询备案信息：先查工信部｜若工信部出错查本地库"""

    icp_biz = IcpBiz()
    result = icp_biz.query(**payload)
    print("备案查询结果为：", result)

    # 查备案信息成功　｜　用备案单位识别归属地信息
    result['data'] = result.get('data', {})
    if result['data'].get('sponsor', '') and result['data'].get('sponsor') != '未备案':
        area = icp_biz.recognize_area(result['data']['sponsor'])
    else:
        area = {'city': '', 'city_code': None, 'region': '', 'region_code': None}
    print("识别的归属地信息为：", area)
    result['data'].update(area)
    return jsonify({
        'status': True,
        'data': result
    }), 201
