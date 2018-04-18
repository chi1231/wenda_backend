# coding=utf-8

from functools import wraps

from rest_framework.response import Response
from rest_framework.status import *

from utils.ip import get_ip
from utils.key_value import GROUP_ADMIN, GROUPS_PROPERTY
from utils.key_value import GROUP_STEWARD
from utils.response_content import NOT_LOGIN, NOT_PROPERTY
from utils.response_content import USER_DOES_NOT_EXIST


def need_steward(view):
    @wraps(view)
    def check_steward(*args, **kwargs):
        if args[1].user.is_deleted:
            return Response({'content': USER_DOES_NOT_EXIST})
        if not args[1].user.is_authenticated():
            return Response({"content": NOT_LOGIN}, status=401)
        if not args[1].user.groups.filter(name=GROUP_STEWARD).exists():
            return Response({'content': NOT_PROPERTY}, status=401)
        return view(*args, **kwargs)

    return check_steward


def need_property_management(view):
    @wraps(view)
    def check_property_role(*args, **kwargs):
        if args[1].user.is_deleted:
            return Response({'content': USER_DOES_NOT_EXIST})
        if not args[1].user.is_authenticated():
            return Response({"content": NOT_LOGIN}, status=401)
        if not args[1].user.groups.filter(name__in=GROUPS_PROPERTY).exists():
            return Response({'content': NOT_PROPERTY}, status=401)
        return view(*args, **kwargs)

    return check_property_role


def need_property_admin(view):
    @wraps(view)
    def check_property_admin(*args, **kwargs):
        if args[1].user.is_deleted:
            return Response({'content': USER_DOES_NOT_EXIST})
        if not args[1].user.is_authenticated():
            return Response({"content": NOT_LOGIN}, status=401)
        if not args[1].user.groups.filter(name=GROUP_ADMIN).exists() and (
                not args[1].user.is_superuser
        ):
            return Response({'content': NOT_PROPERTY}, status=401)

        return view(*args, **kwargs)

    return check_property_admin


def need_login(view):
    @wraps(view)
    def check_login(*args, **kwargs):
        if not args[1].user.is_authenticated():
            return Response(status=HTTP_401_UNAUTHORIZED)
        if args[1].user.is_deleted:
            return Response(status=HTTP_401_UNAUTHORIZED)
        return view(*args, **kwargs)

    return check_login


def need_admin_login(view):
    @wraps(view)
    def check_login(*args, **kwargs):
        if not args[1].user.groups.filter(name=GROUP_ADMIN).exists() and (
                not args[1].user.is_superuser
        ):
            return Response({"status": "error", "content": u'非管理员'}, status=401)
        return view(*args, **kwargs)

    return check_login


def need_super_user(view):
    @wraps(view)
    def check_login(*args, **kwargs):

        if not args[1].user.is_authenticated():
            return Response({"content": "not login"}, status=401)
        if args[1].user.is_deleted:
            return Response({"content": "用户已被删除"}, status=401)
        if not args[1].user.is_superuser:
            return Response({"content": "not super user"}, status=401)
        return view(*args, **kwargs)

    return check_login


def need_login_super(view):
    @wraps(view)
    def check_login(*args, **kwargs):

        if not args[1].user.is_superuser:
            return Response({"content": "not superuser"}, status=401)
        if args[1].user.is_deleted:
            return Response({"content": "用户已被删除"}, status=401)

        return view(*args, **kwargs)

    return check_login


def is_admin(view):
    @wraps(view)
    def check_admin(*args, **kwargs):
        if not args[1].user.clubprofile.all().exists():
            return Response({"content": "not administor"}, status=401)
        return view(*args, **kwargs)

    return check_admin


def operation_log(arg):
    def _operation_log(view):
        @wraps(view)
        def log(*args, **kwargs):
            ip = get_ip(args[1])
            user = args[1].user
            device_uuid = args[1].data.get('device_uuid', 'unknown')
            ua = args[1].META['HTTP_USER_AGENT']
            if 'iPhone' in ua:
                mobile_type = 'iPhone'
            elif 'Macintosh' in ua:
                mobile_type = 'Macintosh'
            elif 'Windows' in ua:
                mobile_type = 'Windows'
            elif 'Android' in ua:
                mobile_type = 'Android'
            elif 'Postman' in ua:
                mobile_type = 'Postman'
            else:
                mobile_type = 'unknown'
            OperationLog.objects.create(type=arg, user=user, ip=ip, device_uuid=device_uuid, mobile_type=mobile_type,
                                        ua=ua)
            return view(*args, **kwargs)

        return log

    return _operation_log
