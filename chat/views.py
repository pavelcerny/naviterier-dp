from django.http import HttpResponse
from django.shortcuts import render

import requests

import json
from watson_developer_cloud import ConversationV1

GOOGLE_API_KEY = "AIzaSyC7WCaTEPswl2Cs77ncqxiz7O4fLK2z2Wk"

conversation = ConversationV1(
  username='8df4159f-bfda-48f4-9827-c331200caebd',
  password='lpULJnXdW2mx',
  version='2017-02-03'
)


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


def poi(request):
    return render(request, 'chat/poi-chat.html')


def gpsAndCompass(request):
    return render(request, 'chat/gpsandcompass.html')


def showCompass(request):
    return render(request, 'chat/showcompass.html')


# API

# process user input
def processUserInput(request):
    text = 'Default reply to user input'
    if (request.method == 'POST'):
        text = 'asked:' + request.POST.get("question")
    return HttpResponse(text)


# return address
def getAddress(request):
    URL = "https://maps.googleapis.com/maps/api/geocode/json"

    # request google API
    payload = {'latlng': request.GET['lat'] + "," + request.GET['lon'],  # 50.094265,
               'key': GOOGLE_API_KEY}
    url = URL
    r = requests.get(url, params=payload)
    data = r.text

    # parse json data
    data = json.loads(data)

    # get object with "lat" and "lng"
    address = data['results'][0]['formatted_address']

    # to String
    response_json = json.dumps(address)
    return HttpResponse(response_json)


# get Watson conversation response
def watsonResponse(request):
    context = {}
    text = ''
    if ('context' in request.session):
        context = request.session['context']
    if ('text' in request.POST):
        text = request.POST['text']

    workspace_id = 'e3101b6f-4808-4630-afbe-b07744997c20'

    response = conversation.message(
        workspace_id=workspace_id,
        message_input={'text':text},
        context=context
    )

    text = json.dumps(response)
    request.session['context'] = response['context']
    return HttpResponse(text)


# get GPS coords from Address
def googleGeocodoingAPI(request):
    API_KEY = GOOGLE_API_KEY
    URL = "https://maps.googleapis.com/maps/api/geocode/json"
    address = request.GET['address']

    # request google API
    payload = {'address': address}
    url = URL
    r = requests.get(url, params=payload)
    data = r.text

    # parse json data

    # EXAMPLE RESPONSE
    #     {
    #     "results": [
    #         {
    #             "address_components": [
    #                 ...
    #             ],
    #             "formatted_address": "Karlovo nám. 319/3, Nové Město, 120 00 Praha-Praha 2, Czechia",
    #             "geometry": {
    #                 "location": {
    #                     "lat": 50.0739567,
    #                     "lng": 14.4185332
    #                 },
    #                 ...
    #             },
    #             ...
    #         }
    #     ],
    #     "status": "OK"
    # }
    data = json.loads(data)

    # get object with "lat" and "lng"
    location = data['results'][0]['geometry']['location']

    # to String
    response_json = json.dumps(location)
    return HttpResponse(response_json)
