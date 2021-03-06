"""SimpleClubManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from main_app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),  # redirect to django admin page
    url(r'^accounts/', include('django.contrib.auth.urls')),  # self manage profiles page
    url(r'^i18n/', include('django.conf.urls.i18n')),  # does the langauge check (1st browser, then user input)
]

"""
Routing for all app specific pages and function like to delete a member.
e.g.: members/(?P<member_id>[0-9]+)/$
all url's are named to have access to them within the code in other locations like views.py
"""
urlpatterns += i18n_patterns(
    url(r'^$', views.index, name='loggedInLandingPage'),
    url(r'^members/add/$', views.add_member, name='add_member'),
    url(r'^members/$', views.list_members, name='list_members'),
    url(r'^members/(?P<member_id>[0-9]+)/$', views.list_member, name='list_member'),
    url(r'^members/(?P<member_id>[0-9]+)/delete/$', views.delete_member, name='delete_member'),
    url(r'^members/(?P<member_id>[0-9]+)/edit/$', views.edit_member, name='edit_member'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^invoices/$', views.list_invoices, name='list_invoices'),
    url(r'^invoices/(?P<invoice_id>[0-9]+)/edit/$', views.edit_invoice, name='edit_invoice'),
    url(r'^invoices/create/$', views.create_invoice, name='create_invoice'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^ice_slots/$', views.list_ices, name='list_ices'),
    url(r'^ice_slots/(?P<ice_slot_id>[0-9]+)/$', views.view_ice, name='view_ice'),
    url(r'^ice_slots/add/$', views.add_ice, name='add_ice'),
    url(r'^ice_slots/(?P<ice_slot_id>[0-9]+)/edit/$', views.edit_ice, name='edit_ice'),
    url(r'^ice_slots/(?P<ice_slot_id>[0-9]+)/delete/$', views.delete_ice, name='delete_ice'),
    url(r'^impressum/', views.impressum, name='impressum'),
    url(r'^accounts/create/', views.create_account, name='create_account'),
    url(r'^trainings/$', views.list_trainings, name='list_trainings'),
    url(r'^trainings/(?P<training_id>[0-9]+)/$', views.view_training, name='view_training'),
    url(r'^trainings/(?P<training_id>[0-9]+)/unregister/$', views.unregister_from_training, name='unregister_from_training'),
    url(r'^trainings/add/$', views.add_training, name='add_training'),
    url(r'^trainings/(?P<training_id>[0-9]+)/edit/$', views.edit_training, name='edit_training'),
    url(r'^trainings/(?P<training_id>[0-9]+)/delete/$', views.delete_training, name='delete_training'),
)
