from django.conf.urls import patterns, url, include

from . import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^shop', views.shop, name='shop'),
    url(r'^order_confirm', views.order_confirm, name='order_confirm'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^logout', views.log_out, name='logout'),
    url(r'^login', views.auth_login, name='auth_login'),
    url(r'^accounts/register', views.registration_register, name='register'),
    url(r'^accounts/registration_activate/([0-9]{15})', views.activate, name='registration_activate'),
    url(r'^sms/$', 'truck_queue.views.sms'),
    url(r'^demo', views.demo, name='demo'),
)

