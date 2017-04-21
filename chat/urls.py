from django.conf.urls import url

import apis.google_api
import apis.views
import apis.watson_api
from . import views

urlpatterns = [
    # views
    url(r'^$', views.index_html, name='index'),
    url(r'^whistory$', views.chat_with_history, name='w_history'),
    url(r'^speech$', views.speechrecognition02, name='speech'),
    url(r'^reversegc$', views.reverseGeocoding, name='reversegeocoding'),
    url(r'^poi$', views.poi, name='poi'),
    url(r'^gps$', views.gpsAndCompass, name='gpsandcompass'),
    url(r'^showcompass$', views.showCompass, name='showCompass'),
    url(r'^clicker$', views.mapClicker, name='clicker'),
    url(r'^navigate$', views.navigate, name='navigate'),


    # API
    url(r'^process$', views.processUserInput, name='process_request'),
    url(r'^address-from-gps$', apis.views.getAddressFromGpsAPI, name='get_address'),
    url(r'^conversation$', apis.views.watsonResponse, name='watson_response'),
    url(r'^googlegeocoding$', apis.views.getGpsFromAddressAPI, name='google_geo'),



]