import json
import requests

from project.api.models import Setting
from project.api.bizs.base import BaseBiz


class ModelAssessmentBiz(BaseBiz):
    def __init__(self):
        super().__init__()
        self.server = self.load_settings()['ai_industry']

    def load_settings(self):
        settings = self.session.query(Setting).filter_by(group='service').all()
        return {setting.name: setting.value for setting in settings}

    def query(self, **kwargs):
        response = requests.get(self.server + '/model_assessment/category/list')
        data = json.loads(response.text)
        res = {}
        res['legend'] = ["F1", "召回率", "准确率"]
        res['seriesData'] = [data['data']['f1'], data['data']['recall'], data['data']['precision']]
        res['xAxisData'] = data['data']['datetime']
        res['title_name'] = {"title": "模型评估", 'xAxisName': "时间", 'yAxisName': '单位(%)'}
        return res
