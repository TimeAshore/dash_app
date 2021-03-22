import json

from project.api.utils.services.base import BaseService


class AI_Industry_Service(BaseService):
    def __init__(self):
        super().__init__()
        self.server = self.settings['ai_industry']

    def classification(self, text):
        try:
            data = {
                "text": text
            }
            headers = {"Content-Type": "application/json"}
            answer_dict = self.get('/category/get_industries', headers=headers, data=json.dumps(data))
            return answer_dict['data']
        except Exception as e:
            print(e)
            return ''
