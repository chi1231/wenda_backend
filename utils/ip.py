# coding=utf-8


def get_ip(request):
    if 'HTTP_X_REAL_IP' in request.META:
        return request.META['HTTP_X_REAL_IP']
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        return request.META['HTTP_X_FORWARDED_FOR']
    if 'REMOTE_ADDR' in request.META:
        return request.META['REMOTE_ADDR']
