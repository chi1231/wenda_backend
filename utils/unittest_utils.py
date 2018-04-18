#!/usr/bin/env python
# encoding: utf-8

from django.contrib.auth.models import Group

from account.models import User


def generate_user(user_data, group_name=None):
    """
    user_data,用户信息字典
    """
    user = User.objects.create(**user_data)
    user.set_password(user_data['password'])
    user.save()
    if group_name:
        group, ok = Group.objects.get_or_create(name=group_name)
        group.user_set.add(user)
    return user
