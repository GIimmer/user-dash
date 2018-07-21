from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.login_register),
    url(r'^register/process$', views.register),
    url(r'^signin/process$', views.signin),
    url(r'^books$', views.allBooks),
    url(r'^books/(?P<book_id>\d+)$', views.book),
    url(r'^books/add$', views.addBook),
    url(r'^books/(?P<book_id>\d+)/review$', views.process_add_review),
    url(r'^books/add/process$', views.process_add_book),
    url(r'^users/(?P<user_id>\d+)$', views.user),
    url(r'^users/(?P<book_id>\d+)/(?P<review_id>\d+)/remove$', views.process_rem_review),
    url(r'^users/logoff$', views.logOff),
]