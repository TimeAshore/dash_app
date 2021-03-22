from flask import Blueprint, jsonify

ping_blueprint = Blueprint('ping', __name__)
payload_location = ('json',)


@ping_blueprint.route('/ping')
def ping():
    return jsonify({
        "status": True
    })
