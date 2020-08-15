from django.conf.urls import url, include
from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/register/$', views.register, name="accounts_register"),
    url(r'^accounts/settings/personal/$', views.settings_personal, name="accounts_settings_personal"),
    url(r'^accounts/settings/email/$', views.settings_email, name="accounts_settings_email"),
    url(r'^accounts/settings/email/change/$', views.change_email),
    url(r'^accounts/settings/email/change/preferences/$', views.change_email_pref),
    url(r'^accounts/settings/password/$', views.settings_password, name="accounts_settings_password"),
    url(r'^accounts/settings/password/change/$', views.change_password),
    url(r'^accounts/settings/password/forget/$', views.forget_password),
    url(r'^accounts/settings/password/reset/(?P<token>[\w-]+)/$', views.reset_password),
    url(r'^accounts/settings/submissions/page/(?P<page_number>[0-9]+)/$', views.show_submissions),
    url(r'^accounts/settings/contests/page/(?P<page_number>[0-9]+)/$', views.show_contests),
    url(r'^accounts/settings/personal/change/profile/$', views.change_profile),
    url(r'^accounts/settings/personal/change/profile/photo/$', views.change_profile_photo),
    url(r'^accounts/profile/(?P<username>[\w-]+)/$', views.profile, name='accounts_profile'),
    url(r'^accounts/verify/(?P<token>[\w-]+)/$', views.verify_accounts, name='verify_accounts'),
    #url(r'^accounts/verification/test/$', views.verify_test, name='verify_accounts_test'),
]