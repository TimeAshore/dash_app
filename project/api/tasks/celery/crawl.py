import requests

from ..base import socweb
from project import create_app
from project.api.models import db, WebsiteNews, Setting


def crawl_website():
    """
    调爬虫服务
    :return:
    """
    settings = db.session.query(Setting).all()
    settings = {setting.name: setting.value for setting in settings}

    urls = db.session.query(WebsiteNews.url).filter_by(ip=None).all()
    print(len(urls))
    url_list = [x[0] for x in urls if '_' not in x[0]]
    print(len(url_list))

    # 不用切割
    data = {
        "namespace": "socmap",
        "url_list": url_list,
        "enable_callback": True,
        "callback_mode": "url",
        "callback_target": settings['runserver'] + "/website/news/callback"
    }
    requests.post(settings['cache_dispatch'] + '/crawl-task/add', json=data, timeout=10)


@socweb.task(queue='discover')
def callback(payload):
    app = create_app()
    app.app_context().push()

    settings = db.session.query(Setting).all()
    settings = {setting.name: setting.value for setting in settings}

    for x in payload['result']:
        try:
            url = x['url']

            # 取缓存
            response = requests.post(settings['cache_query'] + '/cache/get-by-url', json={"url": url},
                                     timeout=10).json()
            ip = response['data']['_source']['server_ip']
            title = response['data']['_source']['title']
            status_code = response['data']['_source']['response_code']
            content = response['data']['_source']['content']
            effective_url = response['data']['_source']['effective_url']

            print(response['data']['_source']['server_ip'])

            # 增加ip,title,status,content
            website_new = db.session.query(WebsiteNews).filter_by(url=url).first()
            website_new.ip = ip
            website_new.title = title
            website_new.http_status = status_code
            website_new.content = content
            website_new.effective_url = effective_url
        except Exception as e:
            print("爬取回调异常：", e)
            continue
        finally:
            try:
                db.session.commit()
            except:
                db.session.rollback()
