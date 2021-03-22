"""
临时脚本
漏了主域id，补上
"""
import requests
import psycopg2

from project import create_app
from project.api.models import db, WebsiteNews, DomainArchived


def get_domain():

    conn = psycopg2.connect(host="192.168.199.17", port="5432", database="socamas", user="postgres", password="123456")
    cur = conn.cursor()
    cur.execute("select name, id from domain_archived")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def callback():
    app = create_app()
    app.app_context().push()

    domains = get_domain()
    for x in domains:
        name, id = x[0], x[1]

        websites = db.session.query(WebsiteNews).filter_by(domain=name).all()
        print('======', name, id, len(websites))
        for w in websites:
            w.domain_id = id
    try:
        db.session.commit()
    except:
        db.session.rollback()


callback()


