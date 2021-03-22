import requests

from project.api.models import Setting
from project.api.models import db, City, Region


class IcpBiz:
    def __init__(self):
        self.session = db.session
        self.settings = self.load_settings()
        self.server = self.settings['icp_server']

    def query(self, domain, captcha="", token=""):
        result = self.post('/query', json={
            'domain': domain,
            'captcha': captcha,
            'token': token
        })
        result['data']['icp_number'] = result['data']['icp']
        del result['data']['icp']
        return result

    def load_settings(self):
        settings = self.session.query(Setting).filter_by(group='service').all()
        return {setting.name: setting.value for setting in settings}

    def get(self, url, **kwargs):
        return self.request('{}{}'.format(self.server, url), method='get', **kwargs)

    def post(self, url, **kwargs):
        return self.request('{}{}'.format(self.server, url), method='post', **kwargs)

    def request(self, url, method='post', timeout=20, **kwargs):
        try:
            resp = requests.request(method, url, timeout=timeout, **kwargs)
        except Exception as e:
            raise Exception(e)
        if resp.status_code != 200:
            raise Exception('服务出错: {}, {}'.format(resp.status_code, resp.text))
        try:
            data = resp.json()
        except Exception as e:
            raise Exception('response format error: {}'.format(e))
        return data

    def get_captcha(self):
        result = self.get('/captcha')
        return result['data']

    def recognize_region(self, text, regions):
        '''
        识别二级归属地
        :param text: 归属单位
        :param regions: 可能的二级归属地
        :return:
        '''

        for region in regions:
            if not region.keywords:
                keywords = [region.name[:-1]] if len(region.name) > 2 else [region.name]
            else:
                keywords = region.keywords  # # 使用二级地区关键词识别
            for keyword in keywords:
                if keyword in text:
                    return region

    def recognize_city(self, text):
        """
        识别一级归属地
        :param text: 归属单位
        :return:
        """
        cities = self.session.query(City).filter(City.name.notin_(['中国', '省直'])).all()
        for city in cities:
            keywords = city.keywords
            for keyword in keywords:  # 使用城市名关键词识别
                if keyword in text:
                    return city

    def recognize_area(self, text):
        """
        识别归属地信息
        :param text: 归属单位
        :return:
        """
        result = {
                'city': '', 'city_code': None,
                'region': '', 'region_code': None
        }
        city, region = None, None
        city = self.recognize_city(text)
        if city:
            # successful, recognize region of the city
            regions = self.session.query(Region).filter_by(city_name=city.name).all()
            region = self.recognize_region(text, regions)
        else:
            # failed, recognize region of all cities
            regions = self.session.query(Region).filter(Region.city_name.notin_(['省直'])).all()
            region = self.recognize_region(text, regions)

        if region:
            # 有二级区域 | 可能有一级
            result.update({'region': region.name, 'region_code': region.code})
            if city:
                result.update({'city': city.name, 'city_code': city.code})
            else:
                # 使用二级区域查出一级归属地
                _city = self.session.query(City).filter_by(name=region.city_name).first()
                result.update({'city': _city.name, 'city_code': _city.code})
            return result
        elif city:
            # only city, no region
            return {
                'city': city.name, 'city_code': city.code,
                'region': '', 'region_code': None
            }
        else:
            # no city, no region
            if '河南' in text:
                #
                return {'city': '省直', 'city_code': '410000', 'region': '省直', 'region_code': '410001'}
            return {
                'city': '', 'city_code': None,
                'region': '', 'region_code': None
            }

