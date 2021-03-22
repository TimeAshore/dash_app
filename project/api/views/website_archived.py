from flask import Blueprint, jsonify
from webargs.flaskparser import use_args
from project.api.schemas.website_archived import add_website_archived_args, update_website_archived_args, \
    query_website_archived_args, update_shown_fields_schema, delete_website_archived_args
from project.api.bizs.website_archived_biz import WebsiteArchivedBiz
from project.api.bizs.setting_biz import SettingBiz


website_archived_blueprint = Blueprint('website_archived', __name__, url_prefix='/website/archived')
payload_location = ('json',)


@website_archived_blueprint.route('', methods=['POST'])
@use_args(add_website_archived_args, locations=payload_location)
def add_website_archive(args):
    website_archive_business = WebsiteArchivedBiz()
    data = website_archive_business.website_archive_add(args)
    return jsonify({
        "status": True, "data": data
    }), 201


@website_archived_blueprint.route('', methods=['PATCH'])
@use_args(update_website_archived_args, locations=payload_location)
def update_website_archive(args):
    website_archive_business = WebsiteArchivedBiz()
    data = website_archive_business.website_archive_update(args)
    return jsonify({
        "status": True, "data": data
    }), 201


@website_archived_blueprint.route('', methods=['DELETE'])
@use_args(delete_website_archived_args, locations=payload_location)
def delete_website_archive(args):
    website_archive_business = WebsiteArchivedBiz()
    website_archive_business.website_archive_delete(args)
    return jsonify({
        "status": True
    }), 204


@website_archived_blueprint.route('/list', methods=['POST'])
@use_args(query_website_archived_args, locations=payload_location)
def query_website_archive(args):
    website_archive_business = WebsiteArchivedBiz()
    data = website_archive_business.query_archive_website(args)
    return jsonify({
        "status": True, "data": data
    }), 201


@website_archived_blueprint.route('/show/field', methods=['GET'])
def get_show_field():
    setting_bussiness = SettingBiz()
    data = setting_bussiness.get_website_archived_setting2()
    return jsonify({
        "status": True, "data": data
    }), 200


@website_archived_blueprint.route('/show/field', methods=['PATCH'])
@use_args(update_shown_fields_schema, locations=payload_location)
def update_show_field(args):
    setting_bussiness = SettingBiz()
    data = setting_bussiness.update_website_archived_setting2(args)
    return jsonify({
        "status": True, "data": data
    }), 201
