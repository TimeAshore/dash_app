from flask import Blueprint, jsonify
from webargs.flaskparser import use_args
from project.api.schemas.domain_archived import add_domain_archived_args, delete_domain_archived_args, \
    update_domain_archived_args, update_shown_fields_schema, query_domain_archived_args
from project.api.bizs.domain_archived_biz import DomainArchivedBiz
from project.api.bizs.setting_biz import SettingBiz


domain_archived_blueprint = Blueprint('domain_archived', __name__, url_prefix='/domain/archived')
payload_location = ('json',)


@domain_archived_blueprint.route('', methods=['POST'])
@use_args(add_domain_archived_args, locations=payload_location)
def add_domain_archive(args):
    domain_archive_business = DomainArchivedBiz()
    data = domain_archive_business.domain_archive_add(args)
    return jsonify({
        "status": True, "data": data
    }), 201


@domain_archived_blueprint.route('', methods=['DELETE'])
@use_args(delete_domain_archived_args, locations=payload_location)
def delete_domain_archive(args):
    domain_archive_business = DomainArchivedBiz()
    domain_archive_business.domain_archive_delete(args)
    return jsonify({
        "status": True
    }), 204


@domain_archived_blueprint.route('', methods=['PATCH'])
@use_args(update_domain_archived_args, locations=payload_location)
def update_domain_archive(args):
    domain_archive_business = DomainArchivedBiz()
    data = domain_archive_business.domain_archive_update(args)
    return jsonify({
        "status": True, "data": data
    }), 201


@domain_archived_blueprint.route('/list', methods=['POST'])
@use_args(query_domain_archived_args, locations=payload_location)
def query_domain_archive(args):
    domain_archive_business = DomainArchivedBiz()
    data = domain_archive_business.query_archive_domain(args)
    return jsonify({
        "status": True, "data": data
    }), 201


@domain_archived_blueprint.route('/show/field', methods=['GET'])
def get_show_field():
    setting_bussiness = SettingBiz()
    data = setting_bussiness.get_domain_archived_setting2()
    return jsonify({
        "status": True, "data": data
    }), 200


@domain_archived_blueprint.route('/show/field', methods=['PATCH'])
@use_args(update_shown_fields_schema, locations=payload_location)
def update_show_field(args):
    setting_bussiness = SettingBiz()
    data = setting_bussiness.update_domain_archived_setting2(args)
    return jsonify({
        "status": True, "data": data
    }), 201
