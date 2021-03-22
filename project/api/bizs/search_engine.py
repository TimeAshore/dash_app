import requests

from .base import BaseBiz
from project.api.models import Setting


class SearchEngineBiz(BaseBiz):

    def __init__(self):
        super(SearchEngineBiz, self).__init__()
        self.allow_query_all = True
        self.settings = self.load_settings()
        self.server = self.settings['search_engine']

    def load_settings(self):
        settings = self.session.query(Setting).filter_by(group='service').all()
        return {setting.name: setting.value for setting in settings}

    def single_dispatch(self, domain):
        """
            'http://192.168.199.220:9700/api/search/subdomain'
        """
        res = requests.post(self.server + '/api/search/subdomain', json={"domain": domain})
        return {
            'length': res.json()['data']['length'],
            'subdomains': res.json()['data']['subdomains']
        }

    def get_subdomain(self):
        """
            'http://192.168.199.220:9700/api/subdomains/query'
        """
        res = requests.post(self.server + '/api/subdomains/query', json={"query_all": True})
        return {
            'length': res.json()['data']['length'],
            'subdomains': res.json()['data']['subdomains']
        }

    def dispatch(self, domains):
        """
            'http://192.168.199.220:9700/api/dispatch/domains'
        """
        res = requests.post(self.server + '/api/dispatch/domains', json={"domains": domains})
        return {
            'http_code': res.status_code
        }

