# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_answer_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='tag',
        ),
        migrations.AddField(
            model_name='question',
            name='tag',
            field=models.CharField(blank=True, max_length=500, default='no_tag'),
        ),
    ]
