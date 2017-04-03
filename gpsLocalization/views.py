import json
from django.http import HttpResponse
from django.shortcuts import render

import requests


# helpers
def getNaviterierData(lat, lon, radius):
    url = "http://147.32.81.71/NaviTerier.ProcessingService/json/reply/FindSourceData"
    payload = {
        'SearchOrigin': {
            'Latitude': lat,
            'Longitude': lon
        },
        'Radius': radius,
    }
    headers = {'content-type': 'application/json'}

    serialized_data = json.dumps(payload)
    # request naviterier api
    r = requests.post(url, data = serialized_data)
    data = r.json()

    return data


def getSegments(naviterierData):
    return naviterierData['Segments']


def getOnlySidewalks(segments):
    sidewalks = []
    for element in segments:
        if element['FormOfWay'] == "Sidewalk":
            sidewalks.append(element)
    return sidewalks


# API
def demo(request):
    object = getNaviterierData(50.0792784,14.4204132, 30)
    object = getSegments(object)
    object = getOnlySidewalks(object)
    return HttpResponse(json.dumps(object), content_type="application/json")


def getSegmentsAPI(request):
    lat = request.POST['lat']
    lon = request.POST['lon']
    radius = request.POST['radius']
    object = getSegments(getNaviterierData(lat, lon, radius))
    return HttpResponse(json.dumps(object), content_type="application/json")


def getSidewalksAPI(request):
    lat = request.POST['lat']
    lon = request.POST['lon']
    radius = request.POST['radius']
    object = getOnlySidewalks(getSegments(getNaviterierData(lat, lon, radius)))
    return HttpResponse(json.dumps(object), content_type="application/json")



def getMap(request):
    mapElements = "map elements gonna be here"
    return HttpResponse(mapElements)



def getSidewalksGrouped(request):
    return NotImplemented


def whereAmI(request):
    address = "Názevulice, kde stojím 7"
    response_json = json.dumps(address)
    return HttpResponse(response_json)