from webargs.flaskparser import use_args
from flask import Blueprint, jsonify, request

from project.api.bizs import WebsiteNewsBiz
from project.api.tasks.celery import deal_subs, generater_search, crawl_website, callback, filter_website, mend_website, auto
from project.api.schemas.website_news import query_args, add_args, filter_args, mend_args, archived_args, update_args, ban_args, delete_args

website_news_blueprint = Blueprint('website_news', __name__)
payload_location = ('json',)


@website_news_blueprint.route('/website/news/auto', methods=['POST'])
def auto_process():
    """
    Generate && Crawl && Filter && Mend
    :return:
    """
    auto.delay()
    return jsonify({
        "status": True
    }), 201


@website_news_blueprint.route('/website/news/generate', methods=['POST'])
def generate_website_archive():
    """
    Call search_engine/brute/FDNS
    :return:
    """
    # deal_subs.delay()
    generater_search.delay()
    return jsonify({
        "status": True
    }), 201


@website_news_blueprint.route('/website/news/crawl', methods=['POST'])
def crawl():
    """
    爬取网站
    :return:
    """
    crawl_website()
    return jsonify({
        "status": True,
    }), 201


@website_news_blueprint.route('/website/news/callback', methods=['POST'])
def crawl_callback():
    """
    爬虫回调
    :return:
    """
    callback.apply_async(args=(request.get_json(),), countdown=10)
    return jsonify({
        "status": True,
    }), 201


@website_news_blueprint.route('/website/news/filter', methods=['POST'])
@use_args(filter_args)
def filter(payload):
    """
    过滤网站
    :param payload:
    :return:
    """
    filter_website.delay(payload)
    return jsonify({
        "status": True,
    }), 201


@website_news_blueprint.route('/website/news/mend', methods=['POST'])
@use_args(mend_args)
def mend(payload):
    """
    补全网站
    :param payload:
    :return:
    """
    mend_website.delay(payload)
    return jsonify({
        "status": True,
    }), 201


@website_news_blueprint.route('/website/news/list', methods=['POST'])
@use_args(query_args, locations=payload_location)
def website_list(payload):
    """
    新发现列表
    :param payload:
    :return:
    """
    websitenews_biz = WebsiteNewsBiz()
    data = websitenews_biz.query(**payload)
    return jsonify({
        "status": True,
        "data": data
    }), 201


@website_news_blueprint.route('/website/news/add', methods=['POST'])
@use_args(add_args)
def add_discovered_websites(payload):
    """
    添加一个新发现
    :param payload:
    :return:
    """
    websitenews_biz = WebsiteNewsBiz()
    websitenews_biz.add(url=payload['url'].strip('/'))
    return jsonify({
        "status": True
    }), 201


@website_news_blueprint.route('/website/news/archived', methods=['POST'])
@use_args(archived_args)
def archived(payload):
    """
    归档
    :param payload:
    :return:
    """
    website_news_biz = WebsiteNewsBiz()
    website_news_biz.archived(payload)
    return jsonify({
        "status": True,
    }), 201


@website_news_blueprint.route('/website/news/update', methods=['PATCH'])
@use_args(update_args)
def update(payload):
    """
    修改
    :param payload:
    :return:
    """
    website_news_biz = WebsiteNewsBiz()
    website_news_biz.update(payload)
    return jsonify({
        "desc": "修改成功",
        "status": True,
    }), 201


@website_news_blueprint.route('/website/news/ban', methods=['POST'])
@use_args(ban_args)
def ban(payload):
    """
    拉黑
    :param payload:
    :return:
    """
    website_news_biz = WebsiteNewsBiz()
    website_news_biz.ban(payload)
    return jsonify({
        "status": True,
    }), 201


@website_news_blueprint.route('/website/news/delete', methods=['DELETE'])
@use_args(delete_args)
def delete(payload):
    """
    删除
    :param payload:
    :return:
    """
    website_news_biz = WebsiteNewsBiz()
    website_news_biz.delete(payload)
    return jsonify({
        "status": True,
    }), 201


@website_news_blueprint.route('/website/news/clear', methods=['DELETE'])
def clear():
    """
    清空
    :return:
    """
    website_news_biz = WebsiteNewsBiz()
    website_news_biz.clear()
    return jsonify({
        "desc": "数据已清空",
        "status": True,
    }), 201

