import json
from datetime import datetime

from django.http import HttpResponse

# Create your views here.
from dpp.functions import loadTrip, loadStop_time, loadCalendar_date, loadRoute, loadShape, loadStop, loadCalendar, \
    loadAgency, loadCSVToModel
from dpp.models import Trip, Route, Stop_time


def update(request):
    loadCSVToModel("agency.txt", "agency_id", loadAgency)
    loadCSVToModel("calendar.txt", "service_id", loadCalendar)
    loadCSVToModel("calendar_dates.txt", "service_id", loadCalendar_date)
    loadCSVToModel("routes.txt", "route_id", loadRoute)
    # loadCSVToModel("shapes.txt", "shape_id", loadShape)
    loadCSVToModel("trips.txt", "route_id", loadTrip)
    loadCSVToModel("stops.txt", "stop_id", loadStop)
    loadCSVToModel("stop_times.txt", "trip_id", loadStop_time)

    return HttpResponse("load ok")


def gpsFromTripleAPI(request):
    startStopName = "Slavia"
    startStopDirection = "Strašnická"
    startLineNumber = "7"

    if ('startStopName' in request.POST):
        startStopName = request.POST['startStopName']
    if ('startStopDirection' in request.POST):
        startStopDirection = request.POST['startStopDirection']
    if ('startLineNumber' in request.POST):
        startLineNumber = request.POST['startLineNumber']

    response = gpsFromTriple(startStopName, startStopDirection, startLineNumber)

    return HttpResponse(json.dumps(response), {'content-type':'application/json'})



def gpsFromTriple(stopName, directionName, lineNumber):
    # find the routes of given tram line
    route = Route.objects.get(route_short_name=lineNumber)
    # find possible headsigns of given tramline
    headsigns = Trip.objects.filter(route=route).order_by('trip_headsign').values('trip_headsign').distinct()


    for hs in headsigns:
        hs_val = hs['trip_headsign']

        # find all rides with given headsign
        query_headsigns = Trip.objects.filter(route=route, trip_headsign=hs_val)

        n_trips = query_headsigns.count()

        # find a ride somewhere in the middle of the day (probably will have less exceptions then the last or first ride)
        tripInHsDirection = query_headsigns[int(n_trips/2)]
        # find all stops on this ride
        query = Stop_time.objects.filter(trip=tripInHsDirection)

        # find a stop with stopName
        query_stop = query.filter(stop__stop_name__contains=stopName)
        # find a stop with directionName
        query_direction = query.filter(stop__stop_name__contains=directionName)

        stop = None
        direction = None

        # trip goes through startStopName
        if query_stop.count()>0:
            stop = query_stop.first()

        # trip goes to startStopDirection
        if query_direction.count()>0:
            direction = query_direction.first()


        if stop != None and direction != None:
            # startStopName and direction is present in this trip
            if stop.stop_sequence < direction.stop_sequence:
                # correct direction
                response = {
                    "name": stop.stop.stop_name,
                    "lat": stop.stop.stop_lat,
                    "lon": stop.stop.stop_lon,
                }
                return response

    return None
