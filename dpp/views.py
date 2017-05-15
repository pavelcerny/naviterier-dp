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
    loadCSVToModel("shapes.txt", "shape_id", loadShape)
    loadCSVToModel("trips.txt", "route_id", loadTrip)
    loadCSVToModel("stops.txt", "stop_id", loadStop)
    loadCSVToModel("stop_times.txt", "trip_id", loadStop_time)

    return HttpResponse("load ok")


def find(request):
    startStopName = "Lazarská"
    startStopDirection = "Václavské náměstí"
    startLineNumber = "9"

    # time = datetime.strptime('7:00:00', '%H:%M:%S')

    response = findFromTriple(startStopName,startStopDirection,startLineNumber)

    return HttpResponse(json.dumps(response))



def findFromTriple(startStopName,startStopDirection,startLineNumber):
    # find tram line details
    route = Route.objects.get(route_short_name=startLineNumber)
    # find all trips with given line, get all their head signs
    headsigns = Trip.objects.filter(route=route).order_by('trip_headsign').values('trip_headsign').distinct()

    for hs in headsigns:
        hs_val = hs['trip_headsign']
        tripInHsDirection = Trip.objects.filter(route=route, trip_headsign=hs_val).last()
        query = Stop_time.objects.filter(trip=tripInHsDirection)

        query_stop = query.filter(stop__stop_name__contains=startStopName)
        query_direction = query.filter(stop__stop_name__contains=startStopDirection)

        stop = None
        direction = None
        if query_stop.count()>0:
            stop = query_stop.first()

        if query_direction.count()>0:
            direction = query_direction.first()

        if stop != None and direction != None:
            # stop and direction is present in this trip
            if stop.stop_sequence < direction.stop_sequence:
                # correct direction
                response = {
                    "name": stop.stop.stop_name,
                    "lat": stop.stop.stop_lat,
                    "lon": stop.stop.stop_lon,
                }
                return response

    return None
