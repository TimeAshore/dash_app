from flask import Blueprint, jsonify
from webargs.flaskparser import use_args
from project.api.bizs.setting_biz import SettingBiz
from project.api.schemas.setting import update_system_schema, update_service_schema

setting_blueprint = Blueprint('setting', __name__, url_prefix='/setting')
payload_location = ('json',)


@setting_blueprint.route('/system', methods=['PATCH'])
@use_args(update_system_schema, locations=payload_location)
def update_system_setting(args):
    setting_bussiness = SettingBiz()
    data = setting_bussiness.update_group_settings(args, group="system")
    return jsonify({
        "status": True, "data": data
    }), 201


@setting_blueprint.route('/system', methods=['GET'])
def get_system_setting():
    setting_bussiness = SettingBiz()
    data = setting_bussiness.get_group_settings(group="system")
    return jsonify({
        "status": True, "data": data
    }), 200


@setting_blueprint.route('/service', methods=['PATCH'])
@use_args(update_service_schema, locations=payload_location)
def update_service_setting(args):
    setting_bussiness = SettingBiz()
    data = setting_bussiness.update_group_settings(args, group="service")
    return jsonify({
        "status": True, "data": data
    }), 201


@setting_blueprint.route('/service', methods=['GET'])
def get_service_setting():
    setting_bussiness = SettingBiz()
    data = setting_bussiness.get_group_settings(group="service")
    return jsonify({
        "status": True, "data": data
    }), 200
