import os
import re
import json
from webargs.flaskparser import use_args
from flask import Blueprint, jsonify, send_file, send_from_directory, make_response

from project.config import DevelopmentConfig
from project.api.tasks.celery import export_data
from project.api.schemas.export import export_schema


export_blueprint = Blueprint('export', __name__)
payload_location = ('json', 'query')


@export_blueprint.route('/export', methods=['GET', 'POST'])
@use_args(export_schema, locations=payload_location)
def export(payload):
    if payload.get('filter'):
        filter = json.loads(payload.get('filter'))
        payload['filter'] = filter
    res = export_data.delay(payload)
    while not res.ready():
        pass
    filename = res.result

    file_path = '{}/{}/{}'.format(DevelopmentConfig.PROJECT_PATH,
                                  DevelopmentConfig.EXPORT_PATH.split('.')[-1].strip('/'), filename)
    if not os.path.isfile(file_path):
        return jsonify(code=400, desc='无此文件')

    return send_file(file_path, as_attachment=True)


# @export_blueprint.route('/download/<string:filename>', methods=['GET'])
# def download_file(filename):
#     if not re.match('^[0-9]+\.xlsx$', filename):
#         return jsonify(code=400, desc='无此文件')
#     file_path = '{}/{}/{}'.format(DevelopmentConfig.PROJECT_PATH,
#                                   DevelopmentConfig.EXPORT_PATH.split('.')[-1].strip('/'), filename)
#     if not os.path.isfile(file_path):
#         return jsonify(code=400, desc='无此文件')
#
#     return send_file(file_path, as_attachment=True)
#
#     # directory = '{}/{}/'.format(DevelopmentConfig.PROJECT_PATH, DevelopmentConfig.DOWNLOAD_PATH)
#     # response = make_response(send_from_directory(directory, filename, as_attachment=True))
#     # response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
#     # return response

