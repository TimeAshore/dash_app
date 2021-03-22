from .base import BaseBiz
from project.api.models import BanKeyword, BanGroup


class FilterSettingBiz(BaseBiz):

    def __init__(self):
        super(FilterSettingBiz, self).__init__()
        self.model = BanKeyword
        self.allow_query_all = True

    def get_group(self):
        """
        获取关键词列表
        :return:
        """
        groups = self.session.query(BanGroup).all()
        return [{'id': x.id, 'name': x.name} for x in groups]

    def delete_group(self, payload):
        """
        删除关键词分组
        :return:
        """
        group = self.session.query(BanGroup).filter_by(id=payload['id']).first()
        self.session.delete(group)
        self.safe_commit()

    def add_group(self, payload):
        """
        新建关键词分组
        :return:
        """
        group_new = BanGroup(**payload)
        self.session.add(group_new)
        self.safe_commit()

    def delete(self, payload):
        """
        删除
        :param payload: id 列表
        :return:
        """
        for id in payload.get('ids', []):
            website = self.session.query(BanKeyword).filter_by(id=id).first()
            self.session.delete(website)
            self.safe_commit()

    def add(self, payload):
        """
        添加
        :param payload:
        :return:
        """
        ban_new = BanKeyword(**payload)
        self.session.add(ban_new)
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
        if condition.get('keyword'):
            query = query.filter(self.model.keyword.ilike('%' + condition['keyword'] + '%'))
        if condition.get('groups'):
            query = query.filter(self.model.group.in_(condition['groups']))
        if condition.get('typs'):
            query = query.filter(self.model.typ.in_(condition['typs']))
        return query


