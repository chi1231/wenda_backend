# coding=utf-8
import re
import time
from datetime import date
from datetime import datetime
from datetime import timedelta


def strtime(timestamp):
    time_array = time.localtime(timestamp)
    other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return other_style_time


def now():
    n = datetime.now()
    return int(time.mktime(n.timetuple()))


def now_string():
    n = datetime.now()
    return n.strftime("%Y-%m-%d %H:%M:%S")


def get_min_day(stamp):
    d = datetime.fromtimestamp(stamp)
    min_d = datetime.combine(d, datetime.min.time())
    return int(time.mktime(min_d.utctimetuple()))


def get_max_day(stamp):
    d = datetime.fromtimestamp(stamp / 1000)
    min_d = datetime.combine(d, datetime.max.time())
    return int(time.mktime(min_d.utctimetuple())) * 1000


def get_one_day_stamp():
    """ 获取一天的时间戳大小 """
    return 86400000


def get_specific_minute_stamp(minute):
    """获取具体分钟数的时间戳大小"""
    minute = int(minute)
    return minute * 60


def get_min_week(stamp):
    """  获取一个周的周一的时间戳的大小 """
    stamp = get_min_day(stamp)
    d = datetime.fromtimestamp(stamp / 1000)
    return stamp - get_one_day_stamp() * d.weekday()


def get_next_week_date():
    """  获取一个周的周一的时间戳的大小 """
    today = datetime.now()
    return (today + timedelta(days=7 - today.weekday())).date()


def get_min_month(stamp):
    """  获取一个月的月初的时间戳的大小 """
    stamp = get_min_day(stamp)
    d = datetime.fromtimestamp(stamp / 1000)
    return stamp - get_one_day_stamp() * (d.day - 1)


def check_code(code):
    pattern = re.compile('[0-9A-Z]')
    if len(pattern.findall(code)) == len(code):
        return True
    return False


def get_last_month_first_day_date(last_month_count):
    """ 获取几个月前的月初日期"""

    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    new_year = now.year - last_month_count / 12
    month_count = last_month_count % 12
    new_month = now.month - month_count
    if new_month < 1:
        new_month += 12
        new_year -= 1
    return now.replace(year=new_year, month=new_month, day=1)


def get_stamp(date, hour=0, minute=0, second=0):
    d = datetime.strptime(date, "%Y-%m-%d")
    d = d.replace(hour=hour, minute=minute, second=second, microsecond=0)

    return int(time.mktime(d.timetuple())) * 1000


def get_today_stamp():
    return int(time.mktime(date.today().timetuple()))


def get_today_str():
    return date.today().strftime("%Y-%m-%d")


def get_month_stamp(year, month):
    if month <= 0:
        year = year - abs(month) / 12 - 1
        month = 12 - abs(month) % 12
    if month > 12:
        year += month / 12
        month = month % 12
    d = datetime.strptime(str(year) + '-' + str(month) + '-' + '1', "%Y-%m-%d")
    d = d.replace(hour=0, minute=0, second=0, microsecond=0)
    return int(time.mktime(d.timetuple()))


def get_current_week():
    # 2016年春季学期第一周起始时间
    start = datetime(2016, 2, 29)
    now = datetime.now()
    return (now - start).days / 7 + 1


def get_cur_date():
    """获取当前的日期"""
    return datetime.today().date()


def get_datetime_from_stamp(timestamp):
    """获取指定时间戳的具体日期"""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def get_date_from_stamp(timestamp):
    """获取指定时间戳的具体日期"""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


def get_start_stamp():
    """获取当天零点的时间戳"""
    today = datetime.today()
    n = datetime(today.year, today.month, today.day, 0, 0, 0)
    return int(time.mktime(n.timetuple()))


def get_end_stamp():
    """获取当天23:59:59秒的时间戳"""
    today = datetime.today()
    n = datetime(today.year, today.month, today.day, 23, 59, 59)
    return int(time.mktime(n.timetuple()))


def get_mons_from_stamp(start_timestamp, end_timestamp):
    """计算两个日期相差的月份"""
    start = time.localtime(start_timestamp)
    end = time.localtime(end_timestamp)
    return (end.tm_year - start.tm_year) * 12 + end.tm_mon - start.tm_mon


def get_day_stamp(date):
    """计算指定年/月/日的时间戳"""
    date = date.timetuple()
    year = date.tm_year
    mon = date.tm_mon
    day = date.tm_mday
    return int(time.mktime(datetime(year, mon, day, 0, 0, 0).timetuple()))


def get_stamp_from_str(str):
    return int(time.mktime(time.strptime(str, "%Y-%m-%d")))
