from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^queue/$', views.queue, name='queue'),
    url(r'^page/(?P<page_number>[0-9]+)/$', views.page, name='page'),
    url(r'^$', views.index, name='index'),
]