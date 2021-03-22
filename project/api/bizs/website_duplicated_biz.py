from .base import BaseBiz
from project.api.models import WebsiteNews, WebsiteDuplicated


class WebsiteDuplicatedBiz(BaseBiz):

    def __init__(self):
        super(WebsiteDuplicatedBiz, self).__init__()
        self.model = WebsiteDuplicated
        self.allow_query_all = True

    def delete(self, payload):
        """
        批量删除
        :param payload: id 列表
        :return:
        """
        for id in payload.get('ids', []):
            website = self.session.query(WebsiteDuplicated).filter_by(id=id).first()
            self.session.delete(website)
            self.safe_commit()

    def restore(self, payload):
        """
        批量还原
        :param payload:　id 列表
        :return:
        """
        for id in payload.get('ids', []):
            website = self.session.query(WebsiteDuplicated).filter_by(id=id).first()
            website_new = WebsiteNews(**website.as_dict())

            self.session.add(website_new)
            self.session.delete(website)
            self.safe_commit()

    def _query(self, payload):
        """
        查询
        :param payload:
        :return:
        """
        query = self.session.query(self.model)
        return self.base_query(query, **payload)

    def _build_query_filter(self, query, condition, strict=False):
        for attr in ['url', 'title', 'effective_url']:
            if condition.get(attr):
                cls_attr = getattr(self.model, attr)
                query = query.filter(cls_attr.ilike('%' + condition[attr] + '%'))
                break
        return query


