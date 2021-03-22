"""
临时脚本
漏了实际地址，补上
"""

import requests
import psycopg2

from project import create_app
from project.api.models import db, WebsiteNews, Setting


def get_urls():

    conn = psycopg2.connect(host="192.168.199.17", port="5432", database="socamas", user="postgres", password="123456")
    cur = conn.cursor()
    cur.execute("select url from website_news")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    urls = [x[0] for x in rows]
    return urls


def callback():
    app = create_app()
    app.app_context().push()

    settings = db.session.query(Setting).all()
    settings = {setting.name: setting.value for setting in settings}


    urls = get_urls()
    for url in urls:
        try:
            # 取缓存
            response = requests.post(settings['cache_query'] + '/cache/get-by-url', json={"url": url}, timeout=10).json()
            effective_url = response['data']['_source']['effective_url']
            print(response['data']['_source']['server_ip'])

            # 增加ip,title,status,content
            website_new = db.session.query(WebsiteNews).filter_by(url=url).first()
            website_new.effective_url = effective_url
        except Exception as e:
            print("爬取回调异常：", response, url)
            continue
    try:
        db.session.commit()
    except:
        db.session.rollback()


callback()
