import time
from ..base import socweb
from project import create_app
from . import deal_subs, generater_search, crawl_website, filter_website, mend_website


@socweb.task(queue='discover')
def auto():
    app = create_app()
    app.app_context().push()

    # 生成
    # deal_subs()
    generater_search()

    # 爬取
    crawl_website()
    time.sleep(60*60)  # callback时间

    # 过滤
    filter_website({})

    # 补全
    mend_website({})

