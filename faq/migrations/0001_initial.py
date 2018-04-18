# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.date_scraper
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('dec', models.CharField(max_length=500)),
                ('img', models.CharField(blank=True, max_length=200)),
                ('zan', models.IntegerField(default=0)),
                ('oppose', models.IntegerField(default=0)),
                ('is_solved', models.BooleanField(default=False)),
                ('created_time', models.BigIntegerField(default=utils.date_scraper.now)),
                ('uuid', models.SlugField(default=uuid.uuid1, unique=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('dec', models.CharField(blank=True, max_length=200)),
                ('img', models.CharField(blank=True, max_length=200)),
                ('is_solved', models.BooleanField(default=False)),
                ('created_time', models.BigIntegerField(default=utils.date_scraper.now)),
                ('uuid', models.SlugField(default=uuid.uuid1, unique=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='questions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', to='faq.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(related_name='answers', to=settings.AUTH_USER_MODEL),
        ),
    ]
