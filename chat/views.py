from django.http import HttpResponse
from django.shortcuts import render

import requests

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def index_html(request):
    return render(request, 'chat/helloworld.html', {})


def chat_with_history(request):
    return render(request, 'chat/whistory.html', {})


def speechrecognition(request):
    return  render(request, 'chat/speechrecognition.html', {})


def speechrecognition02(request):
    return  render(request, 'chat/speechrecognition02.html', {})


def reverseGeocoding(request):
    return render(request, 'chat/reverse-geocoding.html')


# API

# process user input
def processUserInput(request):
    text = 'Default reply to user input'
    if (request.method == 'POST'):
        text = 'asked:' + request.POST.get("question")
    return HttpResponse(text)


# return address
def getAddress(request):
    payload = {'lat': request.GET['lat'], #50.094265,
               'lon': request.GET['lon'], #14.44941,
               'lod': 7}

    url = 'http://cws.ceda.cz/msol-geo-services/services/geocoding/reverse'
    r  = requests.get(url, params=payload)
    data = r.text

    return HttpResponse(data)
