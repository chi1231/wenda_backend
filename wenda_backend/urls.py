from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.response import Response

urlpatterns = [
    # Examples:
    # url(r'^$', 'wenda_backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/account/', include('account.urls')),
    url(r'^api/faq/', include('faq.urls')),
    url(r'^api/img/', include('qiniuyun.urls')),

]

