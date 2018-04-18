from django.conf.urls import *

from .views import ImgTokenView

urlpatterns = patterns(
    '',
    url(r'^token/?$', ImgTokenView.as_view(), name='img_token_view'),

)
