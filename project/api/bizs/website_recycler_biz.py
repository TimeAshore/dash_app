from .base import db, BaseBiz
from project.api.models import WebsiteRecycler, WebsiteArchived
from .setting_biz import SettingBiz

class WebsiteRecyclerBiz(BaseBiz):

    def __init__(self):
        super(WebsiteRecyclerBiz, self).__init__()
        self.model = WebsiteRecycler
        self.allow_query_all = True

    def _query(self, **kwargs):
        return self.query(**kwargs)

    def _build_query_filter(self, query, condition, strict=False):
        for attr in ['url', 'title', 'domain', 'host_dept']:
            if condition.get(attr):
                cls_attr = getattr(self.model, attr)
                query = query.filter(cls_attr.ilike('%' + condition[attr] + '%'))
        return query

    def _build_json_data(self, data, filter_count, total_count, fields=None, **kwargs):
        if fields is None:
            setting_biz = SettingBiz()
            fields = setting_biz.get_website_recycler_setting()['website_recycler_shown_fields']
            print(fields)
        return {
            "records": [self.trans2dict(obj, fields=fields, **kwargs) for obj in data],
            "total_count": total_count,
            "filter_count": filter_count
        }

    def _delete(self, server_info):
        website_recycler_ids = server_info.get('website_recycler_ids')
        for website_recycler_id in website_recycler_ids:
            self.delete(id=website_recycler_id)
        self.safe_commit()

    def _restore(self, server_info):
        website_recycler_ids = server_info.get('website_recycler_ids')
        for website_recycler_id in website_recycler_ids:
            website_recycler = self.find(id=website_recycler_id)
            self.delete(id=website_recycler_id)
            website_archived = WebsiteArchived(**website_recycler.as_dict())
            self.session.add(website_archived)
        self.safe_commit()


