from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^member_add/', views.member_add),
    url(r'^member_directory/', views.member_directory),
    url(r'^member_delete/', views.member_delete),
    url(r'^member_edit/', views.member_edit),
    url(r'^billing/', views.billing),
    url(r'^contact/', views.contact),
    url(r'^ice_management/', views.ice_management),
    url(r'^impressum/', views.impressum),
    url(r'^login/', views.login),
    url(r'^material/', views.material),
    url(r'^trainings/', views.trainings),

]
