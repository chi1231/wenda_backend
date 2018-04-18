from django.conf.urls import *
from .views import QuestionView, QuestionObjectView, AnswerView, AnswerObjectView

urlpatterns = patterns(
    '',
    url(r'^question/(?P<id>\d+)/?$', QuestionObjectView.as_view(), name='question_object_view'),
    url(r'^question/?$', QuestionView.as_view(), name='question_view'),
    url(r'^answer/(?P<id>\d+)/?$', AnswerObjectView.as_view(), name='answer_object_view'),
    url(r'^answer/?$', AnswerView.as_view(), name='answer_view'),
)
