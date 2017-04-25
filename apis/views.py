import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apis import google_api, naviterier_api
from apis.naviterier_api import findRoutes, getItinerary
from apis.watson_api import conversation, WORKSPACE_ID


@csrf_exempt
def getAddressesAPI(request):
        # unpack
        lat = request.GET['lat']
        lon = request.GET['lon']

        # do
        response = naviterier_api.getAddresses(lat, lon)

        # pack
        return HttpResponse(json.dumps(response), content_type="application/json")


def _getFirstItinerary(response):
    error = False
    message = ""

    if "TargetAddress" not in response:
        if "SourceAddress" not in response:
            return "Both Start & Target address is wrongly written. Double check it's correct"
        else:
            return "Target address is wrongly written. Double check it's correct"
    if "SourceAddress" not in response:
        return "Source address is wrongly written. Double check it's correct"

    itinerary = response["Routes"][0]["Itinerary"]
    return itinerary



@csrf_exempt
def findRoutesAPI(request):
    # unpack
    sourceAddress = request.post["SourceAddress"]
    targetAddress = request.post["TargetAddress"]

    # do
    response = findRoutes(sourceAddress, targetAddress)
    
    response = _getFirstItinerary(response)

    # pack
    return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
def getAddressFromGpsAPI(request):
    """ return address from lat lon """
    lat = request.GET['lat']
    lon = request.GET['lon']

    address = google_api.getAddress(lat, lon)

    # to String
    return HttpResponse(address)


@csrf_exempt
def getGpsFromAddressAPI(request):
    """ get GPS coords from Address """
    # extract
    address = request.GET['address']

    # do
    location = google_api.getGps(address)

    # pack
    response_json = json.dumps(location)
    return HttpResponse(response_json)


def getTracing(request):
    # unpack
    sourceAddress = request.GET['TargetAddress']
    tartgetAddress = request.GET['SourceAddress']

    # do
    response = getItinerary(sourceAddress, tartgetAddress)

    # pack
    return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
def watsonResponse(request):
    """ get Watson conversation response"""
    context = {}
    text = ''
    if ('context' in request.session):
        context = request.session['context']
    if ('text' in request.POST):
        text = request.POST['text']

    # workspace_id = 'e3101b6f-4808-4630-afbe-b07744997c20'
    workspace_id = WORKSPACE_ID

    response = conversation.message(
        workspace_id=workspace_id,
        message_input={'text':text},
        context=context
    )

    text = json.dumps(response)
    request.session['context'] = response['context']
    return HttpResponse(text)


@csrf_exempt
def demo(request):
    # unpack
    sourceAddress = "Lazarská 3"
    tartgetAddress = "Myslíkova 13"

    # do
    response = getItinerary(sourceAddress, tartgetAddress)

    # pack
    return HttpResponse(json.dumps(response), content_type="application/json")