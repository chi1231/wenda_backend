from django.conf.urls import *

from account.views import LoginView, LogoutView, ChangePassWord, look_ones_answers, UserObjectView
from account.views import UserView
from account.views import look_ones_questions
from . import views

urlpatterns = patterns(
    '',
    url(r'^login/?$', LoginView.as_view(), name='user_login_view'),
    url(r'^user/?$', UserView.as_view(), name='user_view'),
    url(r'^user/(?P<id>\d+)/?$', UserObjectView.as_view(), name='user_object_view'),
    url(r'^logout/?$', LogoutView.as_view(), name='user_logout_view'),
    url(r'^change_password/?$', ChangePassWord.as_view(), name='change_password_view'),

    url(r'^user/(?P<id>\d+)/questions/?$', look_ones_questions, name='look_ones_questions'),
    url(r'^user/(?P<id>\d+)/answers/?$', look_ones_answers, name='look_ones_answers'),

)
