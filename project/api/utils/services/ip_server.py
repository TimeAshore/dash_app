from project.api.utils.services.base import BaseService


class IPService(BaseService):
    def __init__(self):
        super().__init__()
        self.server = self.settings['ip_server']

    def query(self, ip):
        headers = {"Content-Type": "application/json"}
        result = self.post('/ip/server', headers=headers, json={"ip_list": [ip]})
        return result['data']
