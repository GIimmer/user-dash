from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.landing_page),
    url(r'^register$', views.register),
    url(r'^register/process$', views.processRegister),
    url(r'^signin$', views.signIn),
    url(r'^signin/process$', views.processSignin),
    url(r'^dashboard$', views.displayUsers),
    url(r'^users/new$', views.addUser),
    url(r'^addUser/process$', views.processAddUser),
    url(r'^users/show/(?P<user_id>\d+)$', views.wall),
    url(r'^users/edit/(?P<user_id>\d+)$', views.editUser),
    url(r'^users/edit/(?P<user_id>\d+)/process$', views.processEditUser),
    url(r'^users/logoff$', views.logOff),
    url(r'^users/remove/(?P<user_id>\d+)$', views.processRemove),
    url(r'^users/(?P<user_id>\d+)/addMessage$', views.processMessage),
    url(r'^users/(?P<user_id>\d+)/(?P<message_id>\d+)/addComment$', views.processComment),
    url(r'^users/(?P<user_id>\d+)/deleteMessage$', views.deleteMessage),
]