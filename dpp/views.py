import csv
from datetime import datetime
from time import time

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from dpp.models import Agency, Calendar, Calendar_date, Route, Stop, Stop_time, Trip, Shape

FILE_PATH = "C:/Users/cerny/Documents/fel/DIP/In Python/chat_demo/dpp/dpp_data/"


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


def loadCSVToModel(filename, first_column_name, loadFunction):
    csv_filepathname = FILE_PATH + filename
    with open(csv_filepathname, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        i = 0
        for row in reader:
            if (i/1000) > 1000:
                print(i)
            if row[0] != first_column_name:
                # Ignore the header row, import everything else
                loadFunction(row)


def loadAgency(row):
    agency = Agency()
    agency.agency_id = row[0]
    agency.agency_name = row[1]
    agency.agency_url = row[2]
    agency.agency_timezone = row[3]
    agency.agency_lang = row[4]
    agency.agency_phone = row[5]
    agency.save()


def loadCalendar(row):
    c = Calendar()
    c.service_id = row[0]
    c.monday = row[1]
    c.tuesday = row[2]
    c.wednesday = row[3]
    c.thursday = row[4]
    c.friday = row[5]
    c.saturday = row[6]
    c.sunday = row[7]
    c.start_date = datetime.strptime(row[8],'%Y%m%d')
    c.end_date = datetime.strptime(row[9],'%Y%m%d')
    c.save()


def loadCalendar_date(row):
    cd = Calendar_date()
    cd.service_id = row[0]
    cd.date = datetime.strptime(row[1],'%Y%m%d')
    cd.exception_type = row[2]
    cd.save()


def loadRoute(row):
    r = Route()
    r.route_id = row[0]
    r.agency_id_id = row[1]
    r.route_short_name = row[2]
    r.route_long_name = row[3]
    r.route_type = row[4]
    r.route_color = row[5]
    r.save()


def loadShape(row):
    s = Shape()
    s.shape_id = row[0]
    s.shape_pt_lat = row[1]
    s.shape_pt_lon = row[2]
    s.shape_pt_sequence = row[3]
    s.save()


def loadStop(row):
    s = Stop()
    s.stop_id = row[0]
    s.stop_name = row[1]
    s.stop_lat = row[2]
    s.stop_lon = row[3]
    s.location_type = row[4]
    s.parent_station_id = row[5]
    s.wheelchair_boarding = row[6]
    s.save()


def loadStop_time(row):
    st = Stop_time()
    st.trip_id_id = row[0]
    st.arrival_time = datetime.strptime(parsetime(row[1]),'%H:%M:%S')
    st.departure_time = datetime.strptime(parsetime(row[2]),'%H:%M:%S')
    st.stop_id_id = row[3]
    st.stop_sequence = row[4]
    st.pickup_type = row[5]
    st.drop_off_type = row[6]
    st.save()


def loadTrip(row):
    t = Trip()
    t.route_id_id = row[0]
    t.service_id_id = row[1]
    t.trip_id = row[2]
    t.trip_headsign = row[3]
    t.shape_id_id = row[4]
    t.wheelchair_accessible = row[5]
    t.save()

def parsetime(time_string):
    vals = time_string.split(':')
    vals[0] = int(vals[0]) % 24
    return '{}:{}:{}'.format(vals[0],vals[1],vals[2])