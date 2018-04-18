# coding=utf-8

import datetime

from account.serializers import UserManageSer
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from utils.decorators import need_super_user


def robots(request):
    """禁止所有的爬虫
    """
    return HttpResponse("User-Agent: *\nDisallow: /")


class DashboardView(APIView):
    @need_super_user
    def get(self, request, **kwargs):
        account_count = User.objects.all().count()
        new_account_count = User.objects.filter(
            date_joined__gt=datetime.date.today()).count()
        users = User.objects.all().order_by("-id")[0:50]
        return Response({
            "account_count": account_count,
            "new_account_count": new_account_count,
            "order_count": 0,
            "owe_count": 0,
            "new_users": UserManageSer(users, many=True).data
        })
