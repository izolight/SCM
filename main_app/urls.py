from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^members/add/$', views.add_member, name='add_member'),
    url(r'^members/$', views.list_members, name='list_members'),
    url(r'^members/delete/', views.delete_member, name='delete_member'),
    url(r'^members/edit/', views.edit_member, name='edit_member'),
    url(r'^bills/$', views.list_bills, name='list_bills'),
    url(r'^bills/open/', views.open_bill, name='open_bill'),
    url(r'^bills/facturate/', views.facturate_bill, name='facturate_bill'),
    url(r'^bills/facturated/', views.facturated_bill),
    url(r'^bills/delayed/', views.delayed_bill),
    url(r'^bills/reminded/', views.reminded_bill),
    url(r'^bills/register/', views.register_bill),
    url(r'^bills/notpayed/', views.notpayed_bill),
    url(r'^contacts/', views.contact, name='contact'),
    url(r'^ices/$', views.list_ices, name='list_ices'),
    url(r'^ices/add/', views.add_ice, name='add_ice'),
    url(r'^ices/edit/', views.edit_ice, name='edit_ice'),
    url(r'^ices/delete/', views.delete_ice, name='delete_ice'),
    url(r'^impressums/', views.impressum, name='impressum'),
    url(r'^logins/', views.login, name='login'),
    url(r'^accounts/create', views.create_account),
    url(r'^trainings/$', views.list_trainings, name='list_trainings'),
    url(r'^trainings/add', views.add_training, name='add_training'),
    url(r'^trainings/edit', views.edit_training, name='edit_training'),
    url(r'^trainings/delete', views.delete_training, name='delete_training'),

]
