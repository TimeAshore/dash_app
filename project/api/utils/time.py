# coding: utf-8

from datetime import datetime, timedelta
import time


def utc2locale(date_time, time_format="%Y-%m-%d %H:%M"):
    """
      将UTC时间转换为本地时间
      :param date_time:
      :param time_format:
      :return: local time, "%Y-%m-%d %H:%M:%S"
    """
    if date_time is None:
        return ''
    time = date_time + timedelta(hours=+8)
    return time.strftime(time_format)


def ts2locale(timestamp, time_format="%Y-%m-%d %H:%M"):
    """
      将时间戳转换为本地时间
      :param date_time:
      :param time_format:
      :return: local time, "%Y-%m-%d %H:%M:%S"
    """
    now_ts = timestamp + 8 * 3600
    now_dt = datetime.fromtimestamp(now_ts)
    return now_dt.strftime(time_format)


def str2dt(string_time, locale=True, time_format="%Y-%m-%d %H:%M"):
    """
      将本地时间转换为UTC时间
      :param string_time:
      :param locale:
      :param time_format:
      :return:
    """
    dt = datetime.strptime(string_time, time_format)
    if locale:
        dt = dt + timedelta(hours=-8)  # 中国默认时区
    return dt


def dt2timestamp(dt):
    """
      Datetime转化为TimeStamp
      :param dt:
      :return:
    """
    if isinstance(dt, datetime):
        timestamp = dt.timestamp()
        return int(timestamp)
    return dt


def timestamp2dt(timestamp, locale=False):
    """
      TimeStamp转化为Datetime
      :param timestamp:
      :param locale:
      :return:
    """
    if isinstance(timestamp, (int, float)):
        dt = datetime.utcfromtimestamp(timestamp)
        if locale:  # 是否转化为本地时间
            dt = dt + timedelta(hours=8)  # 中国默认时区
        return dt
    return timestamp


def time_delta_format(time):
    hours = int(time.seconds / 3600)
    minutes = int(time.seconds % 3600 / 60)
    seconds = int(time.seconds % 3600 % 60)
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


def time_duration(date_time):
    if not date_time:
        return 0
    duration = time.time() - date_time.timestamp()
    return int(duration / 86400)
