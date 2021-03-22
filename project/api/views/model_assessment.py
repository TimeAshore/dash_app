from flask import Blueprint, jsonify

from project.api.bizs.model_assessment_biz import ModelAssessmentBiz

model_assessment_blueprint = Blueprint('model_assessment', __name__)


@model_assessment_blueprint.route('/model_assessment/category/list', methods=['GET'])
def get_assessment_category():
    assessment_category_biz = ModelAssessmentBiz()
    data = assessment_category_biz.query()
    return jsonify({
        'data': data,
        'status': True
    }), 200
