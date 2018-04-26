"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from invitations import views as invitations_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', invitations_views.register, name='register'),
    url(r'^$', invitations_views.WelcomeView.as_view(), name='welcome'),
    url(r'^user/(?P<pk>\d+)/$', login_required(invitations_views.AppUserDetailView.as_view()), name='user_profile'),
    url(r'^accounts/login/$', views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^accounts/logout/$', views.logout, name="logout", kwargs={'next_page': '/'}),
    url(r'', include('invitations.urls', namespace="invitations")),
]
