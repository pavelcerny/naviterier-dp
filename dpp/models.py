from django.db import models


class Agency(models.Model):
    agency_id = models.PositiveIntegerField(primary_key=True)
    agency_name = models.CharField(max_length=30)
    agency_url = models.CharField(max_length=30)
    agency_timezone = models.CharField(max_length=30)
    agency_lang = models.CharField(max_length=30)
    agency_phone = models.CharField(max_length=30)


class Calendar(models.Model):
    service_id = models.PositiveIntegerField(primary_key=True)
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()


class Calendar_date(models.Model):
    service_id = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    date = models.DateField()
    exception_type = models.IntegerField()


class Route(models.Model):
    route_id = models.CharField(max_length=12, primary_key=True)
    agency_id = models.ForeignKey(Agency, on_delete=None)
    route_short_name = models.CharField(max_length=12)
    route_long_name = models.CharField(max_length=50)
    route_type = models.IntegerField()
    route_color = models.CharField(max_length=12)


class Shape(models.Model):
    shape_id = models.IntegerField()
    shape_pt_lat = models.FloatField()
    shape_pt_lon = models.FloatField()
    shape_pt_sequence = models.IntegerField()


class Trip(models.Model):
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    trip_id = models.IntegerField(primary_key=True)
    trip_headsign = models.CharField(max_length=30)
    shape_id = models.ForeignKey(Shape, on_delete=None)
    wheelchair_accessible = models.IntegerField()


class Stop(models.Model):
    stop_id = models.CharField(max_length=12, primary_key=True)
    stop_name = models.CharField(max_length=30)
    stop_lat = models.FloatField()
    stop_lon = models.FloatField()
    location_type = models.IntegerField()
    parent_station = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    wheelchair_boarding = models.IntegerField


class Stop_time(models.Model):
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    stop_id = models.ForeignKey(Stop, on_delete=models.CASCADE)
    stop_sequence = models.PositiveIntegerField()
    pickup_type = models.PositiveSmallIntegerField()
    drop_off_type = models.PositiveSmallIntegerField()



