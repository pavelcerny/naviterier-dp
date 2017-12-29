import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apis import google_api, naviterier_api, here_api
from apis.naviterier_api import findRoutes, getItinerary
from apis.watson_api import conversation, WORKSPACE_ID


@csrf_exempt
def getAddressesInNaviterierAPI(request):
    """
    Returns JSON with all addresses stored at the Naviterier server

    :returns dictionary full of addresses
    {"Addresses": [ {"Id": "40825124",
                    "Shape": {"Latitude": 50.0887841946588, "Longitude": 14.4442259626852},
                    "Street": "Pernerova",
                    "HouseNumber": "2b",
                    "LandRegistryNumber": "2870",
                    "City": "Praha"},
                    {...},
                    {...}
    ]}
    """

    response = naviterier_api.getAddresses()

    # pack response
    response_json = json.dumps(response)
    return HttpResponse(response_json, content_type="application/json")


@csrf_exempt
def findRoutesAPI(request):
    '''
    Returns a route's itinerary between SourceAddress and TargetAddress. The route is prepared by Naviterier server.

    :param request: must contain post["SourceAddress"] and post["TargetAddress"]
    :return: JSON with a route dictionary
    '''
    # unpack parameters
    sourceAddress = request.post["SourceAddress"]
    targetAddress = request.post["TargetAddress"]

    # do
    response = findRoutes(sourceAddress, targetAddress)
    
    response = _getFirstItinerary(response)


    # pack response
    response_json = json.dumps(response)
    return HttpResponse(response_json, content_type="application/json")


@csrf_exempt
def getAddressFromGpsAPI(request):
    '''
    return String with address from lat lon
    :param request:
    :return: Street and house number i.e. 'Technická 6'
    '''
    lat = request.GET['lat']
    lon = request.GET['lon']

    # address = google_api.getAddress(lat, lon)
    address = here_api.getAddress(lat, lon)

    # response
    return HttpResponse(address)


@csrf_exempt
def getGpsFromAddressAPI(request):
    '''
    get GPS coords from Address
    :param request:
    :return: json {"lat", "lon"}
    '''
    # extract
    address = request.GET['address']

    # do
    location = google_api.getGps(address)

    # pack response
    response_json = json.dumps(location)
    return HttpResponse(response_json, content_type="application/json")


def getNavigationItineraryFromAddressToAddress(request):
    '''

    :param request:
    :return:
    '''
    # unpack
    sourceAddress = request.GET['SourceAddress']
    tartgetAddress = request.GET['TargetAddress']

    # do
    response = getItinerary(sourceAddress, tartgetAddress)

    # pack response
    response_json = json.dumps(response)
    return HttpResponse(response_json, content_type="application/json")


def getNavigationItineraryFromSegmentIdToAddress(request):
    # unpack
    sourceAddress = request.GET['SourceSegmentId']
    tartgetAddress = request.GET['TargetAddress']

    # do
    response = getItinerary(sourceAddress, tartgetAddress)

    # pack response
    response_json = json.dumps(response)
    return HttpResponse(response_json, content_type="application/json")


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

    # pack response
    request.session['context'] = response['context']
    response_json = json.dumps(response)
    return HttpResponse(response_json, content_type="application/json")


@csrf_exempt
def demo(request):
    # unpack
    sourceAddress = "Lazarská 3"
    tartgetAddress = "Myslíkova 13"

    # do
    response = getItinerary(sourceAddress, tartgetAddress)

    # pack response
    response_json = json.dumps(response)
    return HttpResponse(response_json, content_type="application/json")

