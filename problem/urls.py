from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views
app_label = "problem"
urlpatterns = [
    url(r'^(?P<problem_id>[\w\-]+)/$', views.problem_show, name='problem_show'),
    url(r'^(?P<problem_id>[\w\-]+)/change/$', views.problem_change, name='problem_change'),
    url(r'^(?P<problem_id>[\w\-]+)/submit/$', views.problem_submit, name='problem_submit'),
    url(r'^(?P<problem_id>[\w\-]+)/coq/$', views.coq_show, name='coq_show'),
    url(r'^(?P<problem_id>[\w\-]+)/coq/submit/$', views.coq_submit, name='coq_submit'),
    url(r'^(?P<problem_id>[\w\-]+)/submission/(?P<submission_id>[\w\-]+)/$', views.show_submission, name='show_submission'),
    url(r'^(?P<problem_id>[\w\-]+)/submissions/$', views.problem_submissions, name='problem_submissions'),
]
