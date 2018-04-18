# coding=utf-8

from django.conf.urls import *

from . import views

urlpatterns = patterns(
    '',
    url(r"^dashboard/?$", views.DashboardView.as_view(),
        name='dashboard_view')

)
