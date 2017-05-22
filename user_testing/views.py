import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from gpsLocalization.views import _getUserPathFromLocateMeData
from naviterier.views import gpsForEntryforAddress
from user_testing.models import Experiment, ExperimentType, RecordedBeforeCorner, RecordedAfterCorner


@csrf_exempt
def logExperiment(request):
    lat = 0
    lon = 0
    experimentType = ExperimentType.UNKNOWN
    estimatedAddress = ""
    targetAddress = ""
    userPath = {}

    # unpack
    json_str = request.body
    data = json.loads(json_str)
    # userPath = _getUserPathFromLocateMeData(data)

    if 'lat' in data:
        lat = data['lat']
    if 'lon' in data:
        lon = data['lon']
    if 'experimentType' in data:
        experimentType = data['experimentType']
    if 'estimatedAddress' in data:
        estimatedAddress = data['estimatedAddress']
    if 'targetAddress' in data:
        targetAddress = data['targetAddress']
    if 'userPath' in data:
        userPath = data['userPath']

    entry_coords = gpsForEntryforAddress(estimatedAddress)

    e = Experiment()
    e.type = experimentType
    e.realGpsLat = 0
    e.realGpsLon = 0
    e.estimatedGpsLat = lat
    e.estimatedGpsLon = lon
    e.estimatedAddressLat = entry_coords["lat"]
    e.estimatedAddressLon = entry_coords["lon"]
    e.estimatedAddress = estimatedAddress
    e.targetAddress = targetAddress
    e.recordTime = datetime.datetime.now()
    e.success = False
    e.fromMyTesting = False
    e.save()

    if userPath != {}:
        for u in userPath["beforeCorner"]:
            b = RecordedBeforeCorner()
            b.lat = u["lat"]
            b.lon = u["lon"]
            b.save()
        for u in userPath["afterCorner"]:
            a = RecordedAfterCorner()
            a.lat = u["lat"]
            a.lon = u["lon"]
            a.save()

    # todo save user path

    return HttpResponse('ok')


def viewExperiments(request):
    return None
