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
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    url(r'^$', views.index, name='loggedInLandingPage'),
    url(r'^members/add/$', views.add_member, name='add_member'),
    url(r'^members$', views.list_members, name='list_members'),
    url(r'^members/(?P<member_id>[0-9]+)/$', views.list_member, name='list_member'),
    url(r'^members/(?P<member_id>[0-9]+)/delete/$', views.delete_member, name='delete_member'),
    url(r'^members/(?P<member_id>[0-9]+)/edit/$', views.edit_member, name='edit_member'),
    url(r'^accounts/signup/$', views.signup, name='signup'),
    url(r'^bills$', views.list_bills, name='list_bills'),
    url(r'^bills/(?P<invoice_id>[0-9]+)/open/$', views.open_bill, name='open_bill'),
    url(r'^bills/(?P<invoice_id>[0-9]+)/facturate/$', views.facturate_bill, name='facturate_bill'),
    url(r'^bills/(?P<invoice_id>[0-9]+)/facturated/$', views.facturated_bill, name='facturated_bill'),
    url(r'^bills/(?P<invoice_id>[0-9]+)/delayed/$', views.delayed_bill, name='delayed_bill'),
    url(r'^bills/(?P<invoice_id>[0-9]+)/reminded/$', views.reminded_bill, name='reminded_bill'),
    url(r'^bills/(?P<invoice_id>[0-9]+)/register/$', views.register_bill, name='register_bill'),
    url(r'^bills/(?P<invoice_id>[0-9]+)/notpayed/$', views.notpayed_bill, name='notpayed_bill'),
    url(r'^contacts/$', views.contact, name='contact'),
    url(r'^ices$', views.list_ices, name='list_ices'),
    url(r'^ices/add/$', views.add_ice, name='add_ice'),
    url(r'^ices/(?P<ice_slot_id>[0-9]+)/edit/$', views.edit_ice, name='edit_ice'),
    url(r'^ices/(?P<ice_slot_id>[0-9]+)/delete/$', views.delete_ice, name='delete_ice'),
    url(r'^impressums/', views.impressum, name='impressum'),
    url(r'^accounts/create', views.create_account, name='create_account'),
    url(r'^trainings$', views.list_trainings, name='list_trainings'),
    url(r'^trainings/add$', views.add_training, name='add_training'),
    url(r'^trainings/(?P<training_id>[0-9]+)/edit$', views.edit_training, name='edit_training'),
    url(r'^trainings/(?P<training_id>[0-9]+)/delete$', views.delete_training, name='delete_training'),
)
