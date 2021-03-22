from sqlalchemy import and_

from ..base import socweb
from project import create_app
from project.api.bizs.icp_biz import IcpBiz
from project.api.utils.services.ip_server import IPService
from project.api.models import db, WebsiteNews, Unit, DomainArchived
from project.api.utils.services.ai_industry_server import AI_Industry_Service


@socweb.task(queue='discover')
def mend_website(payload):
    app = create_app()
    app.app_context().push()

    condition(method=payload['condition']) if payload.get('condition', '') else condition()


def mend_website_ip_area():
    """
    调用服务，补全IP归属地
    :return:
    """
    print("开始补全IP归属地...")
    ips = db.session.query(WebsiteNews.ip).filter(and_(WebsiteNews.ip != '', WebsiteNews.ip_area == '')).distinct(WebsiteNews.ip).all()
    ip_service = IPService()
    for ip in ips:
        info = ip_service.query(ip[0])
        ip_area = info[ip[0]]['country'] + '/' + info[ip[0]]['province'] + '/' + info[ip[0]]['city']
        db.session.query(WebsiteNews).filter_by(ip=ip[0]).update({'ip_area': ip_area})
        safe_commit()


def mend_website_host_dept():
    """
    补全归属单位
    :return:
    """
    print("开始补全归属单位...")
    # 同步重点单位
    units = db.session.query(Unit).all()
    for unit in units:
        for domain in unit.domains:
            ws = db.session.query(WebsiteNews).filter(WebsiteNews.url.like(f'%{domain}%')).all()
            if len(ws):
                for w in ws:
                    if '民办高校' in unit.tags:
                        w.host_type = '民营非企业单位'
                        w.host_dept = unit.name
                    elif '有限公司' in unit.name:
                        w.host_type = '企业'
                        w.host_dept = unit.name
                    else:
                        w.host_type = '事业单位'
                        w.host_dept = unit.name
    safe_commit()

    # 给予主域名ICP
    websites = db.session.query(WebsiteNews).filter_by(host_dept='').all()
    for website in websites:
        domain = db.session.query(DomainArchived).filter_by(name=website.domain).first()
        if domain == None:
            print(website.url)
        if domain:
            if domain.sponsor not in ['', '未备案']:
                website.host_dept = domain.sponsor
                website.host_type = domain.sponsor_type
    safe_commit()
    print('补全个数', len(websites))


def mend_website_area():
    """
    补全网站归属地
    （需要先补全归属单位！）
    :return:
    """
    # 同步重点单位归属地
    print("开始补全网站归属地...")
    units = db.session.query(Unit).all()
    for unit in units:
        for domain in unit.domains:
            db.session.query(WebsiteNews).filter(WebsiteNews.url.like('%' + domain + '%'))\
                .update({'city_code': unit.city, 'region_code': unit.region}, synchronize_session=False)
    safe_commit()

    # 由title\ICP识别
    websites = db.session.query(WebsiteNews).filter_by(city_code='').all()
    # websites = db.session.query(WebsiteNews).filter(WebsiteNews.title != '').filter_by(city_code=None).all()
    area_biz = IcpBiz()
    for website in websites:
        area = area_biz.recognize_area(website.host_dept)  # ICP
        if not area['city_code'] and website.title:
            area = area_biz.recognize_area(website.title)  # title
        website.city_code = area['city']
        website.region_code = area['region']

    safe_commit()


def mend_website_industry():
    """
    根据源码补全行业
    :return:
    """
    print("开始补全行业...")
    ai_industry_service = AI_Industry_Service()

    # 有源码 && 行业为空
    websites = db.session.query(WebsiteNews).filter(and_(WebsiteNews.content != '', WebsiteNews.industries == '{}')).all()
    print(len(websites))
    for website in websites:
        industries = ai_industry_service.classification(website.content)
        if industries == '':
            continue

        # 推荐出预测前x(x<=3)名 人工检查修改
        website.ai_industries = website.industries = [industries[x][0].replace("'", '') for x in range(3) if industries[x][1] > 0]
        safe_commit()


def mend_website_type():
    """
    基于title识别网站类型：Web，System
    :return:
    """
    print("开始补全网站类型...")
    websites = db.session.query(WebsiteNews).filter(and_(WebsiteNews.web_type=='', WebsiteNews.title != '')).all()
    for website in websites:
        website.web_type = 'web'
        if ('http://oa' in website.url or 'https://oa' in website.url) or ('系统' in website.title or '登录' in website.title):
            website.web_type = 'system'
    safe_commit()


def mend_website_category():
    """
    补全类别：高等院校、上市公司
    :return:
    """
    print("开始补全网站类别...")
    units = db.session.query(Unit).all()

    for unit in units:
        for domain in unit.domains:
            ws = db.session.query(WebsiteNews).filter(WebsiteNews.url.ilike(f'http%://%{domain}%')).all()
            if len(ws):
                for w in ws:
                    w.category = unit.category
            break
    safe_commit()


def safe_commit():
    try:
        db.session.commit()
    except Exception as e:
        print("补全异常：", e)
        db.session.rollback()


def mend_all():
    """
    补全所有信息
    :return:
    """
    mend_website_ip_area()
    mend_website_host_dept()
    mend_website_area()
    # mend_website_industry()
    mend_website_type()
    mend_website_category()


def condition(method='all'):
    """
    选择补全种类
    :param method:
    :return:
    """
    print(method)
    funcs = {
        'all': mend_all,
        'ip_area': mend_website_ip_area,
        'host_dept': mend_website_host_dept,
        'area': mend_website_area,
        'industry': mend_website_industry,
        'website_type': mend_website_type,
        'category': mend_website_category,
    }
    func = funcs.get(method)
    func()
