from django.conf.urls import url

from . import views

urlpatterns = [
    # views
    # here add the views

    # API
    # url(r'^update$', views.updateAddressesDbAPI, name='updateAdresses'),
    url(r'^log$', views.logExperiment, name='logexperiment'),
    url(r'^$', views.viewExperiments, name='viewExperiments'),
]