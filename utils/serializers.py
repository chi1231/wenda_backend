# coding=utf-8
import datetime

from django.core.exceptions import ValidationError
from pytz import utc
from rest_framework import serializers

from .shortcuts import datetime_to_ms


class MSField(serializers.WritableField):
    """毫秒和datetime之间的互相转换
    """

    def __init__(self, *args, **kwargs):
        super(MSField, self).__init__(*args, **kwargs)
        self.ms = None
        self.datetime = None

    def from_native(self, ms):
        return ms

    def to_native(self, obj):
        if obj:
            if isinstance(obj, int) or isinstance(obj, basestring):
                return datetime.datetime.utcfromtimestamp(int(obj) / 1000).replace(tzinfo=utc)
            else:
                return datetime_to_ms(obj)
        return obj

    def validate(self, value):
        if not isinstance(value, int):
            try:
                int(value)
            except Exception as e:
                raise ValidationError(e)
