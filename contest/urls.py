from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^(?P<contest_id>[\w\-]+)/scoreboard/$', views.scoreboard, name='scoreboard'),
    url(r'^(?P<contest_id>[\w\-]+)/register/$', views.register_contest, name='contest_registeration'),
    url(r'^(?P<contest_id>[\w\-]+)/register/cancel/$', views.register_contest_cancel, name='contest_registeration_cancelation'),
    url(r'^(?P<contest_id>[\w\-]+)/$', views.show, name='show'),
    url(r'^page/(?P<page_number>[0-9]+)/$', views.page, name='page'),
    url(r'^(?P<contest_id>[\w\-]+)/show_json/$', views.show_json, name='show_json'),
    url(r'^$', views.index, name='index'),
]