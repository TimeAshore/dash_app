import requests
from tld import get_fld

from ..base import socweb
from project import create_app
from project.api.bizs import SearchEngineBiz
from project.api.bizs import DomainArchivedBiz
from project.api.models import db, WebsiteNews, DomainArchived


@socweb.task(queue='discover')
def generater_search():
    """
    搜索引擎
    http://192.168.199.220:9700/api/subdomains/query
    :return:
    """
    app = create_app()
    app.app_context().push()

    search_engine_biz = SearchEngineBiz()
    res = requests.post(search_engine_biz.server + '/api/subdomains/query', json={"query_all": True}, timeout=60)

    for url in res.json()['data']['subdomains']:
        domain_name = get_fld(url)
        website_new = WebsiteNews(url=url, domain=domain_name)
        website_new.source = ['search_engine']

        # 赋予主域名id
        domain = db.session.query(DomainArchived).filter_by(name=domain_name).first()
        if domain:
            website_new.domain_id = domain.id

        db.session.add(website_new)
    try:
        db.session.commit()
    except:
        db.session.rollback()


@socweb.task(queue='discover')
def deal_subs():
    """
    爆破
    :return:
    """
    domain_biz = DomainArchivedBiz()
    domains = {
        "domains": domain_biz.get_total_domain()
    }
    response = requests.post(url='http://192.168.199.221/api/socweb/subs', json=domains)
    subs = response.json()['data']
    for sub in subs:
        wensite_news = WebsiteNews()
        wensite_news.url = sub
        wensite_news.source = wensite_news.source.append('brute')
        db.session.add(wensite_news)
    db.session.commit()

