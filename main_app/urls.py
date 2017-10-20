from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^members/add/$', views.add_member, name='add_member'),
    url(r'^members/$', views.list_members, name='list_members'),
    url(r'^members/delete/$', views.delete_member),
    url(r'^members/edit/$', views.edit_member),
    url(r'^billing/$', views.billing),
    url(r'^contact/$', views.contact),
    url(r'^ice_management/$', views.ice_management),
    url(r'^impressum/$', views.impressum),
    url(r'^login/$', views.login),
    url(r'^material/$', views.material),
    url(r'^trainings/$', views.trainings),

]
