from flask import Blueprint, jsonify
from webargs.flaskparser import use_args
from project.api.bizs.stop_word_biz import StopWordBiz
from project.api.schemas.stop_word import delete_stop_word_schema, add_stop_word_schema

stop_word_blueprint = Blueprint('stop_word', __name__, url_prefix='/stop/word')
payload_location = ('json',)


@stop_word_blueprint.route('', methods=['GET'])
def get_stop_word():
    stop_word_bussiness = StopWordBiz()
    data = stop_word_bussiness.query(page=-1)
    return jsonify({
        "status": True, "data": data
    }), 200


@stop_word_blueprint.route('', methods=['DELETE'])
@use_args(delete_stop_word_schema, locations=payload_location)
def delete_stop_word(args):
    stop_word_bussiness = StopWordBiz()
    stop_word_bussiness.delete(args)
    return jsonify({
        "status": True
    }), 204


@stop_word_blueprint.route('', methods=['POST'])
@use_args(add_stop_word_schema, locations=payload_location)
def add_stop_word(args):
    stop_word_bussiness = StopWordBiz()
    data = stop_word_bussiness.add(args)
    return jsonify({
        "status": True, "data": data
    }), 201
