from flask import Blueprint, jsonify
from webargs.flaskparser import use_args

from project.api.bizs.filter_setting_biz import FilterSettingBiz
from project.api.schemas.filter_setting import query_args, delete_args, add_args, delete_group_args, add_group_args

filter_setting_blueprint = Blueprint('filter_setting', __name__)
payload_location = ('json',)


@filter_setting_blueprint.route('/website/filter/setting/query', methods=['POST'])
@use_args(query_args, locations=payload_location)
def query(payload):
    """
    查询
    :param payload:
    :return:
    """
    filter_setting_biz = FilterSettingBiz()
    data = filter_setting_biz._query(payload)

    return jsonify({
        'data': data,
        'status': True
    }), 201


@filter_setting_blueprint.route('/website/filter/setting/delete', methods=['DELETE'])
@use_args(delete_args, locations=payload_location)
def delete(payload):
    """
    删除
    :param payload:
    :return:
    """
    filter_setting_biz = FilterSettingBiz()
    filter_setting_biz.delete(payload)

    return jsonify({
        'status': True
    }), 204


@filter_setting_blueprint.route('/website/filter/setting/add', methods=['POST'])
@use_args(add_args, locations=payload_location)
def add(payload):
    """
    添加
    :param payload:
    :return:
    """
    filter_setting_biz = FilterSettingBiz()
    filter_setting_biz.add(payload)

    return jsonify({
        'status': True
    }), 201


@filter_setting_blueprint.route('/website/filter/setting/group/list', methods=['GET'])
def get_group():
    """
    获取关键词分组列表
    :return:
    """
    filter_setting_biz = FilterSettingBiz()
    data = filter_setting_biz.get_group()

    return jsonify({
        'data': data,
        'status': True
    }), 200


@filter_setting_blueprint.route('/website/filter/setting/group/delete', methods=['DELETE'])
@use_args(delete_group_args, locations=payload_location)
def delete_group(payload):
    """
    删除关键词分组
    :return:
    """
    filter_setting_biz = FilterSettingBiz()
    data = filter_setting_biz.delete_group(payload)

    return jsonify({
        'data': data,
        'status': True
    }), 204


@filter_setting_blueprint.route('/website/filter/setting/group/add', methods=['POST'])
@use_args(add_group_args, locations=payload_location)
def add_group(payload):
    """
    新建关键词分组
    :return:
    """
    filter_setting_biz = FilterSettingBiz()
    filter_setting_biz.add_group(payload)

    return jsonify({
        'status': True
    }), 201

