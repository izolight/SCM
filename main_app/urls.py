from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add_member/', views.add_member),
    url(r'^directory/', views.directory),
]
