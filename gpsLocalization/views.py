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


def getSidewalksPoints(sidewalks):
    sidewalksPoints = []
    for s in sidewalks:
        points = s['Shape']['Points']
        sidewalksPoints.append(points)

    return sidewalksPoints


def mergeSidewalksPoints(sidewalksPoints):
    groups = []
    # add first
    first = sidewalksPoints[0]
    rest = sidewalksPoints[1:]
    groups.append(first)

    for s in rest:
        createNew = True

        # sort into correct group
        for i in range(0, len(groups)):
            # start == start
            if groups[i][0] == s[0]:
                # reverse s
                rev_s = s[::-1]
                # prepend without last
                groups[i] = rev_s[:-1] + groups[i]
                createNew = False
                break
            # start == end
            elif groups[i][0] == s[-1]:
                # prepend without last
                groups[i] = s[:-1] + groups[i]
                createNew = False
                break
            # end == start
            elif groups[i][-1] == s[0]:
                # append without first
                groups[i] = groups[i] + s[1:]
                createNew = False
                break
            # end == end
            elif groups[i][-1] == s[-1]:
                # reverse s
                rev_s = s[::-1]
                # append without first
                groups[i] = groups[i] + rev_s[1:]
                createNew = False
                break
        # begin new group
        if createNew:
            groups.append(s)

    return groups


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


def getGroupedSidewalksAPI(request):
    lat = request.POST['lat']
    lon = request.POST['lon']
    radius = request.POST['radius']
    sidewalks = getOnlySidewalks(getSegments(getNaviterierData(lat, lon, radius)))

    sidewalksPoints = getSidewalksPoints(sidewalks)
    n_groups = len(sidewalksPoints)
    while True:
        sidewalksPoints = mergeSidewalksPoints(sidewalksPoints)
        if len(sidewalksPoints) == n_groups:
            break
        else:
            n_groups = len(sidewalksPoints)

    return HttpResponse(json.dumps(sidewalksPoints), content_type="application/json")



def getMap(request):
    mapElements = "map elements gonna be here"
    return HttpResponse(mapElements)


def whereAmI(request):
    address = "Názevulice, kde stojím 7"
    response_json = json.dumps(address)
    return HttpResponse(response_json)


def locateMeAPI(request):
    log = json.loads(request.body)
    return None