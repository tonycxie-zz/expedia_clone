from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^travels$', views.travels),
    url(r'^logout$', views.logout),
    url(r'^addtrip$', views.add_trip),
    url(r'^new_trip$', views.new_trip),
    url(r'^join/(?P<number>\d+)', views.join),
    url(r'^cancel/(?P<number>\d+)', views.cancel),
    url(r'^delete/(?P<number>\d+)', views.delete),
    url(r'^view/(?P<number>\d+)', views.view)
]