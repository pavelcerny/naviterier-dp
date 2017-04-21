from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def index_html(request):
    return render(request, 'chat/index.html', {})


def chat_with_history(request):
    return render(request, 'chat/whistory.html', {})


def speechrecognition(request):
    return  render(request, 'chat/speechrecognition.html', {})


def speechrecognition02(request):
    return  render(request, 'chat/speechrecognition02.html', {})


def reverseGeocoding(request):
    return render(request, 'chat/proto01-reverse-geocoding.html')


def poi(request):
    return render(request, 'chat/proto02-poi-chat.html')


def gpsAndCompass(request):
    return render(request, 'chat/proto03-gps.html')


def showCompass(request):
    return render(request, 'chat/showcompass.html')


def mapClicker(request):
    return render(request,'chat/clicker.html')


# API

# process user input
def processUserInput(request):
    text = 'Default reply to user input'
    if (request.method == 'POST'):
        text = 'asked:' + request.POST.get("question")
    return HttpResponse(text)


