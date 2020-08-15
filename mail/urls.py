from django.conf.urls import url, include
from . import views
app_name = 'mail'

urlpatterns = [
    url(r'^$', views.view_inbox_first_page),
    url(r'^compose/$', views.compose_mail),
    url(r'^inbox/$', views.view_inbox_first_page),
    url(r'^inbox/id/(?P<mail_id>[0-9]+)/$', views.view_mail),
    url(r'^inbox/page/(?P<page_number>[0-9]+)/$', views.inbox),
    url(r'^sents/$', views.sents),
    url(r'^drafts/$', views.drafts),
    #url(r'^accounts/settings/contests/page/(?P<page_number>[0-9]+)/$', views.show_contests),
    #url(r'^accounts/settings/personal/change/profile/photo/$', views.change_profile_photo),
    #url(r'^accounts/verify/(?P<token>[\w-]+)/$', views.verify_accounts, name='verify_accounts'),
]