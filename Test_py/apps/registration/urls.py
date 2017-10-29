from django.conf.urls import url
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = [
    url(r'Error/$', views.error, name='Error'),
    url(r'Registration/$', views.registration, name='Registration'),
    url(r'Login/$', views.login, name='Login'),
    #url(r'registration_user/$', views.registration_user, name='registration_user'),
    #url(r'^registration/(?P<index>[0-9]+)/$', views.re),
]