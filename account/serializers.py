from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from utils.date_scraper import strtime
from .models import *


class UserLoginSer(serializers.Serializer):
    """登录序列化"""
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)


class ChangePasswordSer(serializers.Serializer):
    """"修改密码序列化"""
    old_password = serializers.CharField(max_length=20)
    new_password = serializers.CharField(max_length=20)


class UserDetailSer(serializers.ModelSerializer):
    register_time = serializers.SerializerMethodField()

    def get_register_time(self, obj):
        return strtime(obj.created_time)

    class Meta:
        model = User
        exclude = ('first_name', 'last_name', 'email', 'is_staff',
                   'groups', 'user_permissions', 'password', 'is_superuser',
                   'date_joined', 'uuid', 'created_time', 'is_deleted')


class UserUpdataSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nick_name', 'desc', 'img')


class UserSampleSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nick_name', 'img')
