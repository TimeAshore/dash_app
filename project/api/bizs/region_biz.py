from .base import BaseBiz
from project.api.models import Region


class RegionBiz(BaseBiz):

    def __init__(self):
        super(RegionBiz, self).__init__()
        self.allow_query_all = True
        self.model = Region

    def _query(self, **kwargs):
        region_code = {'rows': {}}

        regions = self.session.query(Region).filter_by(city_name=kwargs.get('city', '')).all()
        for obj in regions:
            region_code['rows'][obj.name] = obj.code
        region_code['length'] = len(region_code['rows'])
        return region_code
