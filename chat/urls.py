from django.conf.urls import url

from . import views

urlpatterns = [
    # views
    url(r'^$', views.index_html, name='index'),
    url(r'^whistory$', views.chat_with_history, name='w_history'),
    url(r'^speech$', views.speechrecognition02, name='speech'),
    url(r'^reversegc$', views.reverseGeocoding, name='reversegeocoding'),

    # API
    url(r'^process$', views.processUserInput, name='process_request'),
    url(r'^address-from-gps$', views.getAddress, name='get_address'),



]