# coding=utf-8

import logging

logger = logging.getLogger('error_logger')


class LoggerErrorMiddleware(object):
    def process_exception(self, request, exception):
        logger.exception(exception)


class DisableCSRFCheckMiddleware(object):
    """使用这个完全禁用Django的csrf检查 因为Django的csrf检查是可以关掉的，但是Django rest framework的csrf检查没办法关闭
    """

    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

    def process_response(self, request, response):
        response["Access-Control-Allow-Headers"] = "*"
        response["Access-Control-Allow-Methods"] = "*"

        response["Access-Control-Max-Age"] = "60"
        return response
