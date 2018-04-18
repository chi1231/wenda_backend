# coding:utf-8
from rest_framework import permissions

from .key_value import GROUP_ADMIN


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.groups.filter(name=GROUP_ADMIN).exists() and (
                not request.user.is_superuser
        ):
            return False
        else:
            return True
