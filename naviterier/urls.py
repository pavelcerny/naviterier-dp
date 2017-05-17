from django.conf.urls import url

from . import views

urlpatterns = [
    # views
    # here add the views

    # API
    url(r'^update$', views.updateAddressesDbAPI, name='updateAdresses'),
    url(r'^isaddressindb$', views.isAddressInDbAPI, name='isAddressInDb'),
]