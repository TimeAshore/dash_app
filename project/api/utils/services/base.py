import requests

from project.api.models import db, Setting


class BaseService:

    def __init__(self):
        self.ses = db.session
        self.settings = self.load_settings()
        self.server = ""

    def load_settings(self):
        settings = self.ses.query(Setting).all()
        return {setting.name: setting.value for setting in settings}

    def request(self, url, method='post', timeout=20, **kwargs):
        # 调用缓存
        try:
            resp = requests.request(method, url, timeout=timeout, **kwargs)
        except Exception as e:
            print(e)
            # raise ServiceError(e)
        # 缓存出错
        if resp.status_code != 200:
            print("服务出错")
            # raise ServiceError('服务出错: {}, {}'.format(resp.status_code, resp.text))
        # 缓存返回的数据转为json格式
        try:
            data = resp.json()
        except Exception as e:
            print('response format error', e)
            # raise ServiceError('response format error: {}'.format(e))
        # 返回缓存结果
        return data

    def get(self, url, **kwargs):
        return self.request('{}{}'.format(self.server, url), method='get', **kwargs)

    def post(self, url, **kwargs):
        return self.request('{}{}'.format(self.server, url), method='post', **kwargs)

    def safe_commit(self):
        try:
            self.ses.commit()
        except Exception as e:
            self.ses.rollback()
            # raise DBError(e)
        return True
