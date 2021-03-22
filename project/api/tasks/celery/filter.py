from urllib.parse import urlparse
from sqlalchemy import or_, cast, and_, String

from ..base import socweb
from project import create_app
from project.api.models import db, WebsiteNews, BanKeyword, WebsiteBanned, WebsiteArchived, WebsiteDuplicated, \
    WebsiteRecycler


@socweb.task(queue='discover')
def filter_website(payload):
    app = create_app()
    app.app_context().push()

    condition(method=payload['condition']) if payload.get('condition', '') else condition()


def filter_website_with_location():
    """
    根据实际地址与当前url过滤
    :return:
    """
    print("根据实际地址与当前url过滤...")
    websites = db.session.query(WebsiteNews).filter(WebsiteNews.effective_url != '').all()
    for website in websites:
        if urlparse(website.url).netloc != urlparse(website.effective_url).netloc:
            db.session.delete(website)
    safe_commit()


def filter_website_with_status():
    """
    过滤状态不正常的网站，http_status != 200 or http_status == -1
    新发现站点默认状态码 = -1
    :return:
    """
    print("过滤状态不正常的网站...")
    db.session.query(WebsiteNews).filter(or_(WebsiteNews.http_status != 200, WebsiteNews.http_status == -1)).delete()
    safe_commit()


def filter_website_with_internal_ip():
    """
    过滤内网站点
    A类：10.0.0.0～10.255.255.255
    B类：172.16.0.0～172.31.255.255
    C类：192.168.0.0～192.168.255.255
    :return:
    """
    print("过滤内网站点...")
    websites = db.session.query(WebsiteNews).filter(
        or_(
            cast(WebsiteNews.ip, String).like('10.%'),
            and_(WebsiteNews.ip > '172.16.0.0', WebsiteNews.ip <= '172.31.255.255')),
        cast(WebsiteNews.ip, String).like('192.168.%')
    ).all()
    for website in websites:
        db.session.delete(website)
    safe_commit()


def filter_website_with_content():
    """
    根据内容过滤，到黑名单
    :return:
    """
    print("""根据内容过滤...""")
    # 加载关键词列表
    keywords = db.session.query(BanKeyword).filter_by(typ='content').all()
    websites = db.session.query(WebsiteNews).all()
    for website in websites:
        for keyword in keywords:
            # 关键词在内容中，保存到黑名单
            if keyword.keyword in website.content:
                banned_website = WebsiteBanned(**website.as_dict(), group=keyword.group, is_auto=True)

                db.session.add(banned_website)
                db.session.delete(website)
                break

        # if len(website.content) < 1000:  # 这里不对！万一某站点没爬下来源代码，但有http_code且可以打开，就被误删了
        #     # 若content does not contain keywords, delete
        #     # 若源代码里没有这三个关键词，删除
        #     if not any(keyword in website.content for keyword in ['frame', 'script', 'refresh']):
        #         db.session.delete(website)
    safe_commit()


def filter_website_with_title():
    """
    根据title过滤网站，保存到网站黑名单
    :return:
    """
    print("根据title过滤网站...")
    # 加载关键词列表
    keywords = db.session.query(BanKeyword).filter_by(typ='keyword').all()
    websites = db.session.query(WebsiteNews).filter(WebsiteNews.title != '').all()
    for website in websites:
        for keyword in keywords:
            words = keyword.keyword.split('&')

            # 关键词在内容中，保存到黑名单
            if all(word.lower() in website.title.lower() for word in words):
                banned_website = WebsiteBanned(**website.as_dict(), group=keyword.group, is_auto=True)

                db.session.add(banned_website)
                db.session.delete(website)
                break
    safe_commit()


def filter_website_with_ip():
    """
    根据IP过滤网站，保存到网站黑名单
    :return:
    """
    print("根据IP过滤网站...")
    # 加载黑ip
    ips = db.session.query(BanKeyword).filter_by(typ='ip').all()
    for ip in ips:
        websites = db.session.query(WebsiteNews).filter_by(ip=ip.keyword).all()
        for website in websites:
            banned_website = WebsiteBanned(**website.as_dict(), group=ip.group, is_auto=True)

            db.session.add(banned_website)
            db.session.delete(website)

    safe_commit()


def filter_website_with_existed():
    """
    去除其他表中已有的网站，删除
    :return:
    """
    print("去除其他表中已有的网站...")
    websites = db.session.query(WebsiteNews).all()

    for website in websites:
        # 表：已收录、黑名单、重复网站、回收站
        for model in [WebsiteArchived, WebsiteBanned, WebsiteDuplicated, WebsiteRecycler]:
            if db.session.query(model).filter_by(url=website.url).first():
                db.session.delete(website)
                break

    safe_commit()


def filter_website_with_duplicate():
    """
    过滤重复网站, 保存到重复网站
    :return:
    """
    print("过滤重复网站...")
    duplicate1_count = 0  # www与主域名重复的个数
    duplicate2_count = 0  # cftx与主域名重复的个数
    duplicate3_count = 0  # 过滤cftx的个数
    www_count = 0
    other_count = 0

    websites = db.session.query(WebsiteNews).filter(WebsiteNews.title != '').all()
    for (index, website) in enumerate(websites):
        duplicate_exits = False

        if website.url == 'http://www.' + website.domain:
            www_count += 1
            continue
        elif website.url == 'http://' + website.domain:
            # 留http://www.a.com，删http://a.com
            url = 'http://www.{}'.format(website.domain)
            for model in [WebsiteArchived, WebsiteNews]:
                if db.session.query(model).filter_by(url=url, title=website.title).first():  # 指向同一网站，保留http://www.a.com
                    duplicate1_count += 1
                    save_to_duplicate(website)  # http://a.com --> duplicate table
                    break
        elif website.url == 'http://cftx.' + website.domain:
            # 留http://www.a.com||http://a.com，删http://cftx.a.com
            for url in ['http://www.' + website.domain, 'http://' + website.domain]:
                if duplicate_exits:
                    break
                for model in [WebsiteArchived, WebsiteNews]:
                    if db.session.query(model).filter_by(url=url, title=website.title).first():  # 指向同一网站，保留http://www.a.com||http://a.com
                        duplicate2_count += 1
                        save_to_duplicate(website)  # http://cftx.a.com --> duplicate table
                        duplicate_exits = True
                        break
        # 有错，反例：http://www.luoyang.hngp.gov.cn
        else:
            for url in ['http://www.' + website.domain,
                        'http://' + website.domain,
                        'http://cftx.' + website.domain]:
                if duplicate_exits:
                    break
                for model in [WebsiteArchived, WebsiteNews]:
                    if db.session.query(model).filter_by(url=url, title=website.title).first():
                        duplicate3_count += 1
                        save_to_duplicate(website)
                        duplicate_exits = True
                        break
        other_count += 1
    safe_commit()


def safe_commit():
    try:
        db.session.commit()
    except Exception as e:
        print("过滤异常：", e)
        db.session.rollback()


def save_to_duplicate(website):
    """
    Save to duplicate table and delete the website form websitenews.
    :param website:
    :return:
    """
    duplicate_website = WebsiteDuplicated(**website.as_dict(), is_auto=True)
    db.session.add(duplicate_website)

    db.session.delete(website)
    safe_commit()


def filter_all():
    """
    过滤全部条件
    :return:
    """
    filter_website_with_internal_ip()
    filter_website_with_location()
    filter_website_with_existed()
    filter_website_with_content()
    filter_website_with_status()
    filter_website_with_title()
    filter_website_with_ip()
    filter_website_with_duplicate()


def condition(method='all'):
    """
    选择过滤方式
    :param method:
    :return:
    """
    print(method)
    funcs = {
        'all': filter_all,
        'internal_ip': filter_website_with_internal_ip,
        'location': filter_website_with_location,
        'existed': filter_website_with_existed,
        'content': filter_website_with_content,
        'status': filter_website_with_status,
        'title': filter_website_with_title,
        'ip': filter_website_with_ip,
        'duplicate': filter_website_with_duplicate
    }
    func = funcs.get(method)
    func()

