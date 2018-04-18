# coding=utf-8

import datetime
import logging
import time
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import PageNotAnInteger, EmptyPage, InvalidPage
from django.core.paginator import Paginator
from django.utils.timezone import utc
from pytz import utc
from rest_framework import status
from rest_framework.response import Response


# TODO 修改自定义状态码

def warning_logger():
    trace_res = traceback.extract_stack()
    trace = traceback.format_list(trace_res)
    logger = logging.getLogger('warning_logger')
    logger.warning(trace[-3].replace('\n', '', 1))


def http_201_response(data):
    return Response(data=data, status=status.HTTP_201_CREATED)


def http_200_response(data):
    return Response(data={"status_code": 200, "content": data}, status=200)


def http_400_response(error_reason):
    logger = logging.getLogger('warning_logger')
    logger.warning(error_reason)
    warning_logger()
    response = Response(data={"status_code": 400},
                        status=400)
    return response


def http_401_response(error_reason):
    logger = logging.getLogger('warning_logger')
    logger.warning(error_reason)
    warning_logger()
    response = Response(
        data={"status_code": 401, "content": error_reason},
        status=401)
    return response


def ms_to_datetime(ms):
    """将毫秒转换为utc的datetime
    """
    return datetime.datetime.utcfromtimestamp(int(ms) / 1000).replace(tzinfo=utc)


def utc_mktime(utc_tuple):
    """Returns number of seconds elapsed since epoch
    Note that no timezone are taken into consideration.
    utc tuple must be: (year, month, day, hour, minute, second)
    http://stackoverflow.com/questions/5067218/get-utc-timestamp-in-python-with-datetime
    """
    if len(utc_tuple) == 6:
        utc_tuple += (0, 0, 0)
    return time.mktime(utc_tuple) - time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))


def min_to_datetime(min, date=datetime.datetime.utcnow()):
    """将第几分钟转换为某一天的具体datetime
    """
    hour = min / 60
    minute = min % 60
    return datetime.datetime(year=date.year, month=date.month, day=date.day, hour=0, minute=0) + \
           datetime.timedelta(hours=hour, minutes=minute)


def datetime_to_ms(dt):
    return int(utc_mktime(dt.timetuple())) * 1000


def get_time_parameter(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)

    if not (start and end):
        raise ValueError("Parameter start and end are required")
    start_time = ms_to_datetime(start)
    end_time = ms_to_datetime(end)
    if start_time >= end_time:
        raise ValueError("End time must be later than start time")
    return {"start_time": start_time,
            "end_time": end_time,
            "ms_start_time": int(start),
            "ms_end_time": int(end)}


def paginate(request, query_set, object_serializer, pagination_serializer=None, is_need_user=None):
    """
    用于分页的函数
    :param is_need_user: 序列化是否需要传入 request.user
    :param object_serializer: 序列化单个object的serializer 一般只传递这一个就行 自动生成分页的类
    :param pagination_serializer: 如果这个不为None 将使用这个类作为分页工具
    :return:Response
    """
    need_paginate = request.GET.get("paging", None)
    # 如果请求的参数里面没有paging=true的话 就返回全部参数
    if need_paginate != "true":
        return Response(data=object_serializer(query_set, many=True).data)
    page_size = request.GET.get("limit", None)
    if not page_size:
        return http_400_response("Parameter limit is required")
    try:
        page_size = int(page_size)
        if page_size < 1:
            return http_400_response("Invalid limit parameter")
    except (ValueError, TypeError):
        return http_400_response("Invalid limit parameter")
    count = query_set.count()
    paginator = Paginator(query_set, page_size)
    page = int(request.GET.get("page", None))
    try:
        page_data = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        return http_400_response(u"没有更多内容了")
    if pagination_serializer:
        serializer = pagination_serializer(page_data, context={"request": request})
        return Response(data=serializer.data)
    else:
        # 动态定义这样一个类
        if is_need_user:
            return Response({
                "page": page,
                "count": count,
                "results": object_serializer(page_data, many=True, user=request.user).data,
                "limit": page_size
            })

        return Response({
            "page": page,
            "count": count,
            "results": object_serializer(page_data, many=True).data,
            "limit": page_size
        })


def utcnow():
    return datetime.datetime.utcnow().replace(tzinfo=utc)


def get_groupon_code(restaurant, groupon):
    code = int(time.time() * 100)
    return code
