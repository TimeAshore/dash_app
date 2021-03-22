from .base import BaseBiz, db
from project.api.models import Industry


class IndustryBiz(BaseBiz):

    def __init__(self):
        super(IndustryBiz, self).__init__()
        self.model = Industry
        self.allow_query_all = True

    def add(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        ind = Industry(**kwargs)
        self.session.add(ind)
        self.safe_commit()
        return ind.id

    def _query(self):
        industry = self.session.query(Industry).all()
        data = [obj.name for obj in industry]
        return data

