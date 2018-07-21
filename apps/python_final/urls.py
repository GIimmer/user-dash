from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.login),
    url(r'^register/process$', views.processRegister),
    url(r'^signin/process$', views.processSignin),
    url(r'^travels$', views.travels),
    url(r'^addtrip$', views.addTrip),
    url(r'^addtrip/process$', views.processAddTrip),
    url(r'^join/(?P<trip_id>\d+)$', views.joinTrip),
    url(r'^cancel/(?P<trip_id>\d+)$', views.leaveTrip),
    url(r'^delete/(?P<trip_id>\d+)$', views.deleteTrip),
    url(r'^view/(?P<trip_id>\d+)$', views.viewTrip),
    url(r'^logoff$', views.logOff),
]