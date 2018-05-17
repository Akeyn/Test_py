from django.conf.urls import url
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = [
    url(r'Error/$', views.error, name='Error'),
    url(r'Registration/$', views.registration, name='Registration'),
    url(r'Login/$', views.login, name='Login'),
    url(r'Test/$', views.test, name='Test'),
    url(r'Userpage/$', views.userpage, name='Userpage'),
    url(r'Userpage/Edit/$', views.editinfo, name='Editinfo'),
    url(r'Userlist/$', views.userlist, name='Userlist'),
    url(r'Schedule/$', views.schedule, name='Schedule'),
    url(r'Meter/$', views.meter, name='Meter'),
    url(r'Meter/Edit/(?P<meter_id>[0-9]+)/$', views.editmeterinfo, name='EditMeterInfo'),
    url(r'Meter/Delete/(?P<meter_id>[0-9]+)/$', views.deletemeter, name='DeleteMeter'),
    url(r'Meter/History/(?P<meter_id>[0-9]+)/$', views.historymeter, name='HistoryMeter'),
    # url(r'registration_user/$', views.registration_user, name='registration_user'),
    # url(r'^registration/(?P<index>[0-9]+)/$', views.re),
    url(r'Meter/$', views.meter, name='Meter'),
]
