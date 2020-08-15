from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views
app_name = 'blog'
urlpatterns = [
    url(r'^$', views.redirect_to_page, name='redirect_to_page'),
    url(r'^(?P<post_id>[0-9]+)/$', views.index, name='index'),
    url(r'^page/(?P<page_number>[0-9]+)/$', views.page, name='page'),
    url(r'^(?P<post_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/reply/$', views.add_comment, name='add_comment'),
]