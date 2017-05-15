from django.conf.urls import url

from . import views

urlpatterns = [
    # views
    # here add the views

    # API
    url(r'^update$', views.update, name='update'),
    url(r'^find$', views.find, name='find'),

]