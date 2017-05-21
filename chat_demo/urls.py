"""chat_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

# from django.contrib import admin
from django.contrib import admin

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^', include('chat.urls', namespace="chat")),
    url(r'^gpstools/', include('gpsLocalization.urls', namespace="gpsLocalization")),
    url(r'^apis/', include('apis.urls', namespace="apis")),
    url(r'^naviterier/', include('naviterier.urls', namespace="naviterier")),
    url(r'^dpp/', include('dpp.urls', namespace="dpp")),
    url(r'^log/', include('user_testing.urls', namespace="usertesting")),
    url(r'^admin/', admin.site.urls),

]
