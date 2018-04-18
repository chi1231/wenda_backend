import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.date_scraper import now


class User(AbstractUser):
    # 注册唯一手机号
    phone_number = models.CharField(max_length=11, unique=True)
    # 昵称
    nick_name = models.CharField(max_length=10, blank=True)
    # 得赞数
    dezanshu = models.IntegerField(default=0)
    # 个人描述或者一句话简介
    desc = models.CharField(max_length=100, blank=True)
    # 头像
    img = models.CharField(max_length=200, blank=True)
    # 关注 得做成单独的表 manytomany不行

    created_time = models.BigIntegerField(default=now)
    uuid = models.SlugField(default=uuid.uuid1, unique=True)
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.phone_number