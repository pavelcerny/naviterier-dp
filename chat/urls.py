from django.conf.urls import url

import apis.google_api
import apis.views
import apis.watson_api
from . import views

urlpatterns = [
    # development
    url(r'^reversegcdev$', views.reverseGeocoding, name='reversegcDev'),
    url(r'^poidev$', views.poi, name='poiDev'),
    url(r'^gpsdev$', views.gps, name='gpsDev'),

    # final prototypes
    url(r'^reversegc$', views.reverseGeocodingFinal, name='reversegc'),
    url(r'^poi$', views.poiFinal, name='poi'),
    url(r'^gps$', views.gpsFinal, name='gps'),

    # tools
    url(r'^$', views.index_html, name='index'),
    url(r'^whistory$', views.chat_with_history, name='w_history'),
    url(r'^speech$', views.speechrecognition02, name='speech'),
    url(r'^showcompass$', views.showCompass, name='showCompass'),
    url(r'^clicker$', views.mapClicker, name='clicker'),
    url(r'^navigateExample$', views.navigateExample, name='navigateExample'),
    url(r'^navigate$', views.navigateCurrentNaviterier, name='navigate'),
    url(r'^sb$', views.sandbox, name='sandbox'),


    # APIs
    url(r'^process$', views.processUserInput, name='process_request'),
    url(r'^address-from-gps$', apis.views.getAddressFromGpsAPI, name='get_address'),
    url(r'^conversation$', apis.views.watsonResponse, name='watson_response'),
    url(r'^googlegeocoding$', apis.views.getGpsFromAddressAPI, name='google_geo'),



]