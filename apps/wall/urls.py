from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<user_id>\d+)$', views.displayWall),
    url(r'^(?P<user_id>\d+)/message$', views.processMessage),
    url(r'^(?P<user_id>\d+)/comment$', views.processComment),
    url(r'^(?P<user_id>\d+)/message/delete$', views.deleteMessage),
    url(r'^(?P<user_id>\d+)/logOff$', views.logOff),
]