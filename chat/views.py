from django.http import HttpResponse
from django.shortcuts import render

from user_testing.models import ExperimentType


def reverseGeocodingFinal(request):
    context = {
        'type': ExperimentType.REVERSE_GEOCODING
    }
    return render(request, 'chat/fin01-reverse-geocoding.html', context=context)


def poiFinal(request):
    context = {
        'type-address': ExperimentType.POI_ADDRESS,
        'type-mhd': ExperimentType.POI_MHD,
    }
    return render(request, 'chat/fin02-poi-chat.html', context=context)


def gpsFinal(request):
    context = {
        'type': ExperimentType.GPS_COMPASS
    }
    return render(request, 'chat/fin03-gps.html', context=context)


# old methods
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def index_html(request):
    return render(request, 'chat/index.html', {})


def navigateCurrentNaviterier(request):
    return render(request, 'chat/naviterierCurrent.html', {})


def chat_with_history(request):
    return render(request, 'chat/whistory.html', {})


def speechrecognition(request):
    return render(request, 'chat/speechrecognition.html', {})


def speechrecognition02(request):
    return render(request, 'chat/speechrecognition02.html', {})


def reverseGeocoding(request):
    return render(request, 'chat/proto01-reverse-geocoding.html')


def navigateExample(request):
    if "TargetAddress" in request.GET:
        targetAddress = request.GET["TargetAddress"]
        sourceAddress = request.GET["SourceAddress"]
    else:
        targetAddress = "Myslíkova 13"
        sourceAddress = "Lazarská 5"

    if "PreviousUrl" in request.GET:
        previousUrl = request.GET["PreviousUrl"]
    else:
        previousUrl = ""

    context = {
        "TargetAddress": targetAddress,
        "SourceAddress": sourceAddress,
        "PreviousUrl": previousUrl
    }
    return render(request, 'chat/protoFIN-navigate.html', context)


def poi(request):
    # reset session
    request.session['context'] = {}

    return render(request, 'chat/proto02-poi-chat.html')


def gpsAndCompass(request):
    return render(request, 'chat/proto03-gps.html')


def showCompass(request):
    return render(request, 'chat/showcompass.html')


def mapClicker(request):
    return render(request, 'chat/clicker.html')


# API

# process user input
def processUserInput(request):
    text = 'Default reply to user input'
    if (request.method == 'POST'):
        text = 'asked:' + request.POST.get("question")
    return HttpResponse(text)


def sandbox(request):
    return render(request, 'chat/sandbox.html')
