from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_html, name='index'),
    url(r'^whistory$', views.chat_with_history, name='w_history'),
    url(r'^speech$', views.speechrecognition02, name='speech'),


]