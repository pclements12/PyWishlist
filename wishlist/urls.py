"""wishlist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from wishlist_app import urls
from wishlist_app.views import operations
from django.views.generic import TemplateView
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_complete, password_reset_confirm

urlpatterns = [
    # password reset
    url(r'^user/password/reset/$', password_reset, {'post_reset_redirect': '/user/password/reset/sent/',
                                                    'template_name': 'password/password_reset.html'},
        name="password_reset"),
    url(r'^user/password/reset/sent/$', TemplateView.as_view(template_name='password/password_reset_sent.html'),
        name="password_reset_done"),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,
        {'post_reset_redirect': '/user/password/done/',
         'template_name': 'password/password_reset_confirm.html'},
        name="password_reset_confirm"),
    url(r'^user/password/done/$', password_reset_complete,
        {'template_name': 'password/password_reset_complete.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', operations.request_login, name="login"),
    url(r'^wishlist/', include(urls))
]
