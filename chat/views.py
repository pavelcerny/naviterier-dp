from django.http import HttpResponse
from django.shortcuts import render

import requests

import json
from watson_developer_cloud import ConversationV1

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


# get Watson conversation response
def watsonResponse(request):
    context = {}

    workspace_id = 'e3101b6f-4808-4630-afbe-b07744997c20'

    response = conversation.message(
        workspace_id=workspace_id,
        message_input={'text':''},
        context=context
    )

    text = json.dumps(response, indent=2)
    return HttpResponse(text)