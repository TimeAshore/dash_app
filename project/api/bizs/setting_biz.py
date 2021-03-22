import json
from project.api.bizs.base import BaseBiz
from project.api.models import Setting, db
from project.api.exceptions.customs import RecordNotFound


class SettingBiz(BaseBiz):

    def __init__(self):
        super(SettingBiz, self).__init__()
        self.domain_value_dict = {
            "id": "ID",
            "name": "主域名",
            "city_code": "一级归属地",
            "region_code": "二级归属地",
            "icp_number": "ICP备案号",
            "icp_update": "ICP刷新时间",
            "icp_source": "ICP来源",
            "sponsor": "备案单位",
            "sponsor_type": "备案单位性质",
            "invalid_time": "失效时间",
            "industries": "行业",
            "national_level": "国家级",
            "tags": "标签",
            "subdomain_count": "子域名数量",
            "website_count": "网站数量",
            "website_count_updated": "网站数量更新时间",
            "create_time": "主域名创建时间",
            "update_time": "主域名更新时间"
        }
        self.website_value_dict = {
            "id": "ID",
            "url": "网站地址",
            "domain": "主域名",
            "domain_id": "主域名ID",
            "city_code": "一级归属地",
            "region_code": "二级归属地",
            "ip": "IP地址",
            "ip_area": "IP归属地",
            "title": "网站名称",
            "web_type": "网站类型",
            "host_dept": "归属单位",
            "host_type": "单位性质",
            "industries": "行业",
            "ai_industries": "智能分类行业",
            "tags": "标签",
            "code_language": "编程语言",
            "http_status": "网站状态",
            "http_status_list": "网站状态列表",
            "category": "类别",
            "title_updated": "标题更新时间",
            "status_updated": "状态更新时间",
            "create_time": "主域名创建时间",
            "update_time": "主域名更新时间"
        }
        self.model = Setting
        self.session = db.session
        self.allow_query_all = False

    @staticmethod
    def trans_to_value(value, isjson=True):
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            return json.loads(value) if isjson else value

    @staticmethod
    def trans_in_value(value, isjson=True):
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            return json.dumps(value) if isjson else value

    def get_domain_archived_setting(self):
        setting = self.session.query(Setting).filter_by(name='domain_archived_shown_fields').first()
        if not setting:
            raise RecordNotFound('无此配置')

        data = {}
        for value in json.loads(setting.value):
            data[value] = self.domain_value_dict[value]
        return data

    def get_domain_archived_setting2(self):
        setting = self.session.query(Setting).filter_by(name='domain_archived_shown_fields').first()
        if not setting:
            raise RecordNotFound('无此配置')
        return {setting.name: json.loads(setting.value)}

    def update_domain_archived_setting(self, server_info):
        setting = self.session.query(Setting).filter_by(name='domain_archived_shown_fields').first()
        setting.value = json.dumps(server_info['domain_archived_shown_fields'])
        self.safe_commit()

        data = {}
        for value in json.loads(setting.value):
            data[value] = self.domain_value_dict[value]
        return data

    def update_domain_archived_setting2(self, server_info):
        setting = self.session.query(Setting).filter_by(name='domain_archived_shown_fields').first()
        setting.value = json.dumps(server_info['domain_archived_shown_fields'])
        self.safe_commit()

        return {setting.name: json.loads(setting.value)}

    def get_domain_recycler_setting(self):
        setting = self.session.query(Setting).filter_by(name='domain_recycler_shown_fields').first()
        if not setting:
            raise RecordNotFound('无此配置')
        return {setting.name: json.loads(setting.value)}

    def get_website_archived_setting(self):
        setting = self.session.query(Setting).filter_by(name='website_archived_shown_fields').first()
        if not setting:
            raise RecordNotFound('无此配置')

        data = {}
        for value in json.loads(setting.value):
            data[value] = self.website_value_dict[value]
        return data

    def get_website_recycler_setting(self):
        setting = self.session.query(Setting).filter_by(name='website_recycler_shown_fields').first()
        if not setting:
            raise RecordNotFound('无此配置')
        return {setting.name: json.loads(setting.value)}

    def get_website_archived_setting2(self):
        setting = self.session.query(Setting).filter_by(name='website_archived_shown_fields').first()
        if not setting:
            raise RecordNotFound('无此配置')
        print(setting.value)
        return {setting.name: json.loads(setting.value)}

    def update_website_archived_setting(self, server_info):
        setting = self.session.query(Setting).filter_by(name='website_archived_shown_fields').first()
        setting.value = json.dumps(server_info['website_archived_shown_fields'])
        self.safe_commit()

        data = {}
        for value in json.loads(setting.value):
            data[value] = self.website_value_dict[value]
        return data

    def update_website_archived_setting2(self, server_info):
        setting = self.session.query(Setting).filter_by(name='website_archived_shown_fields').first()
        setting.value = json.dumps(server_info['website_archived_shown_fields'])
        self.safe_commit()

        return {setting.name: json.loads(setting.value)}

    def update_group_settings(self, server_info, group='system'):
        for name in server_info:
            setting = self.session.query(Setting).filter_by(group=group, name=name).first()
            if setting:
                setting.value = self.trans_in_value(server_info[name], True if group == 'system' else False)
            else:
                setting = Setting(name=name,
                                  value=self.trans_in_value(server_info[name], True if group == 'system' else False),
                                  group=group)
                self.session.add(setting)
        self.safe_commit()
        settings = self.session.query(Setting).filter_by(group=group).all()
        return {setting.name: self.trans_to_value(setting.value,
                                                  True if group == 'system' else False) for setting in settings}

    def get_group_settings(self, group='system'):
        settings = self.session.query(Setting).filter_by(group=group).all()
        return {setting.name: self.trans_to_value(setting.value, True if group == 'system' else False)
                for setting in settings}

