from .base import BaseBiz, db
from project.api.models import City


class CityBiz(BaseBiz):

    def __init__(self):
        super(CityBiz, self).__init__()
        self.allow_query_all = True
        self.model = City

    def _query(self):
        city_code = {'rows': {}}
        for obj in self.session.query(City).all():
            city_code['rows'][obj.name] = obj.code
        return city_code
