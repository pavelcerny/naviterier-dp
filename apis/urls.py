from django.conf.urls import url

from . import views

urlpatterns = [
    # views
    # here add the views

    # API
    # naviterier
    url(r'^demo$', views.demo, name='demo'),
    url(r'^addresses$', views.getAddressesInNaviterierAPI, name='getaddressesapi'),
    url(r'^routes$', views.findRoutesAPI, name='findroutesapi'),
    url(r'^getItinerary$', views.getItineraryFromAddressToAddressAPI, name='getItinerary'),
    # google
    url(r'^gpsFromAddress$', views.getGpsFromAddressAPI, name='gpsFromAddress'),
    url(r'^addressFromGps$', views.getAddressFromGpsAPI, name='addressFromGps'),
    # watson
    url(r'^watson$', views.watsonResponse, name='watsonResopnse'),


]