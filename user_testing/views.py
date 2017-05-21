import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from gpsLocalization.views import _getUserPathFromLocateMeData
from user_testing.models import Experiment, ExperimentType


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
    #userPath = _getUserPathFromLocateMeData(data)

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


    e = Experiment()
    e.type = experimentType
    e.realGpsLat = 0
    e.realGpsLon = 0
    e.estimatedGpsLat = lat
    e.estimatedGpsLon = lon
    e.estimatedAddressLat = 0
    e.estimatedAddressLon = 0
    e.estimatedAddress = estimatedAddress
    e.targetAddress = targetAddress
    e.recordTime = datetime.datetime.now()
    e.success = False
    e.fromMyTesting = False
    e.save()

    # todo save user path

    return HttpResponse('ok')


def viewExperiments(request):
    return None
