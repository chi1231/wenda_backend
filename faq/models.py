from django.db import models
import uuid
from utils.date_scraper import now
from account.models import User


class Question(models.Model):
    # 标题
    title = models.CharField(max_length=50)
    # 标签分类
    tag = models.CharField(max_length=500, blank=True, default='no_tag')
    # 描述
    dec = models.CharField(max_length=200, blank=True)
    # 图片
    img = models.CharField(max_length=200, blank=True)
    # 提问人
    user = models.ForeignKey(User, related_name='questions')
    # 是否解决
    is_solved = models.BooleanField(default=False)

    created_time = models.BigIntegerField(default=now)
    uuid = models.SlugField(default=uuid.uuid1, unique=True)
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    # 关联的问题
    question = models.ForeignKey(Question, related_name='answers')
    # 关联的用户
    user = models.ForeignKey(User, related_name='answers')
    # 回答
    dec = models.CharField(max_length=500)
    # 图片
    img = models.CharField(max_length=200, blank=True)
    # 得赞数
    zan = models.IntegerField(default=0)
    # 反对数
    oppose = models.IntegerField(default=0)
    # 是否作为推荐回答
    is_solved = models.BooleanField(default=False)

    created_time = models.BigIntegerField(default=now)
    uuid = models.SlugField(default=uuid.uuid1, unique=True)
    is_deleted = models.BooleanField(default=False)


