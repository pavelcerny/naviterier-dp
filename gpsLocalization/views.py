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


def groupSidewalks(sidewalks):

    return NotImplemented


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

    groupsOfSidewalks = groupSidewalks(sidewalks)

    return HttpResponse(json.dumps(object), content_type="application/json")
#     function
#     groupSidewalks(data)
#     {
#         var
#     segments = data;
#
#     var
#     sidewalks = [];
#
#     for (var i in segments) {
#     var segment = segments[i];
#     if (segment.FormOfWay == "Sidewalk") {
#     var sidewalk = {
#     "points": [],
#               "first": [],
#     "last": [],
#     };
#     sidewalk.points = segment.Shape.Points;
#     sidewalk.first = sidewalk.points[0];
#     sidewalk.last = sidewalk.points[sidewalk.points.length - 1];
#     // add
#     sidewalk
#     to
#     the
#     table
#     sidewalks.push(sidewalk);
#     }
#     }
#
#     for (var i = 0; i < sidewalks.length; i++) {
#     if (sidewalks[i] == null) {
#     continue;
#     }
#     for (var j = i+1; j < sidewalks.length; j++) {
#     if (sidewalks[j] == null) {
#     continue;
#     }
#     if (sidewalks[i].first == sidewalks[j].first) {
#
#     // move
#     j - th
#     to
#     i - th
#     sidewalks[i].first = sidewalks[j].last;
#     // todo
#     change
#     order
#     properly
#     // todo
#     don
#     't include the first or last one
#     sidewalks[i].points.append(sidewalks[j].points);
#
#     // delete
#     j - th
#     sidewalks[j] = null;
#
# } else if (sidewalks[i].first == sidewalks[j].last) {
#
# // move
# j - th
# to
# i - th
# sidewalks[i].first = sidewalks[j].first;
# // todo
# change
# order
# properly
# // todo
# don
# 't include the first or last one
# sidewalks[i].points.append(sidewalks[j].points);
#
# // delete
# j - th
# sidewalks[j] = null;
# } else if (sidewalks[i].last == sidewalks[j].first) {
#
# // move
# j - th
# to
# i - th
# sidewalks[i].last = sidewalks[j].last;
# // todo
# change
# order
# properly
# // todo
# don
# 't include the first or last one
# sidewalks[i].points.append(sidewalks[j].points);
#
# // delete
# j - th
# sidewalks[j] = null;
# } else if (sidewalks[i].last == sidewalks[j].last) {
#
# // move
# j - th
# to
# i - th
# sidewalks[i].last = sidewalks[j].first;
# // todo
# change
# order
# properly
# // todo
# don
# 't include the first or last one
# sidewalks[i].points.append(sidewalks[j].points);
#
# // delete
# j - th
# sidewalks[j] = null;
# }
# }
# }
#
# return sidewalks;
# }



def getMap(request):
    mapElements = "map elements gonna be here"
    return HttpResponse(mapElements)



def getSidewalksGrouped(request):
    return NotImplemented


def whereAmI(request):
    address = "Názevulice, kde stojím 7"
    response_json = json.dumps(address)
    return HttpResponse(response_json)