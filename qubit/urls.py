"""qubit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from main.views import handler_error_404, handler_error_500

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('main.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^problem/', include('problem.urls')),
    url(r'^mail/', include('mail.urls')),
    url(r'^contest/', include('contest.urls')),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'main/login.html'}, name='accounts_login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='accounts_logout'),
    url(r'^problemset/', include('problemset.urls')),
]

handler404 = handler_error_404
handler500 = handler_error_500