from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.landingPage),
    url(r'process$', views.process),
    url(r'^(?P<user_id>\d+)/success$', views.success)
]