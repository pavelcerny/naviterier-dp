from django.conf.urls import url

from . import views

urlpatterns = [
    # views
    # here add the views

    # API
    url(r'^$', views.demo, name='demo'),
    url(r'^getsegments$', views.getSegmentsAPI, name='getSegments'),
    url(r'^getsidewalks$', views.getSidewalksAPI, name='getSidewalks'),
    url(r'^getsidewalksgrouped$', views.getGroupedSidewalksAPI, name='getSidewalksGrouped'),
    url(r'^locateme$', views.locateMeAPI, name='locateMeAPI'),
    url(r'^projectionToAddress$', views.getAddressForProjectionAPI, name='getAddressForProjectionApi'),
]