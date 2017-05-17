import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from gpsLocalization import myrepresentation, data
from gpsLocalization.functions import locateMe, getAddressFromProjection
from gpsLocalization.myrepresentation import UserPath


# API

# example of getting data from Naviterier
# return them as json
def demo(request):
    # get some data from sample lat, lon, radius

    # object = naviterier.getData(50.0792784, 14.4204132, 30)
    object = data.getSegments(50.0792784, 14.4204132, 30)
    # object = naviterier_data.getSegmentsJustSidewalks(50.0792784, 14.4204132, 30)
    return HttpResponse(json.dumps(object), content_type="application/json")


# Return Segments, form Naviterir data for given lat, lon, radius
def getSegmentsAPI(request):
    # unpack
    lat = request.POST['lat']
    lon = request.POST['lon']
    radius = request.POST['radius']

    # do
    segments = data.getSegments(lat, lon, radius)

    # pack
    return HttpResponse(json.dumps(segments), content_type="application/json")


# Return only Sidewalks, form Naviterir data for given lat, lon, radius
def getSidewalksAPI(request):
    # unpack
    lat = request.POST['lat']
    lon = request.POST['lon']
    radius = request.POST['radius']

    # do
    sidewalk_segments = data.getSidewalkSegments(lat, lon, radius)

    # pack
    return HttpResponse(json.dumps(sidewalk_segments), content_type="application/json")


# Return array of Sidewalks - each sidewalk consists of multiple objects {lat, lon}
def getGroupedSidewalksAPI(request):
    # unpack
    lat = request.POST['lat']
    lon = request.POST['lon']
    radius = request.POST['radius']

    # do
    sidewalkPaths = data.getPaths(lat, lon, radius)

    # pack
    return HttpResponse(json.dumps(sidewalkPaths), content_type="application/json")


@csrf_exempt
def locateMeAPI(request):
    # unpack
    json_str = request.body
    data = json.loads(json_str)
    userPath = _getUserPathFromLocateMeData(data)

    # do
    user_coordinates, segments_traveled = locateMe(userPath)

    # pack
    api_user_coordinates = myrepresentation.tuple2latlon(user_coordinates)
    #api_segments_traveled = myrepresentation.tuple2Latlon_array(segments_traveled)

    json_object = {
        'userCoordinates': api_user_coordinates,
        'segmentsTraveled': segments_traveled
    }

    return HttpResponse(json.dumps(json_object), content_type="application/json")




def _getUserPathFromLocateMeData(data):
    beforeCorner = data['userPath']['beforeCorner']
    afterCorner = data['userPath']['afterCorner']

    my_beforeCorner = myrepresentation.latlon2tuple_array(beforeCorner)
    my_afterCorner = myrepresentation.latlon2tuple_array(afterCorner)
    my_userPath = UserPath(my_beforeCorner, my_afterCorner)
    return my_userPath


@csrf_exempt
def getAddressForProjectionAPI(request):
    # unpack
    json_str = request.body
    projection = json.loads(json_str)

    # do
    address = getAddressFromProjection(projection)

    # pack
    return_address = "{} {}".format(address["Street"],address["HouseNumber"])
    return HttpResponse(return_address)