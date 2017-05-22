from django.db import models

class ExperimentType():
    UNKNOWN = 0
    REVERSE_GEOCODING = 1
    POI_ADDRESS = 2
    POI_MHD = 3
    GPS_COMPASS = 4

    EXPERIMENT_TYPES = (
        (UNKNOWN, 'Live'),
        (REVERSE_GEOCODING, 'ReverseGeocoding'),
        (POI_ADDRESS, 'PoiAddress'),
        (POI_MHD, 'PoiMhd'),
        (GPS_COMPASS, 'GpsCompass'),
    )

class Experiment(models.Model):
    type = models.IntegerField(choices=ExperimentType.EXPERIMENT_TYPES, default=ExperimentType.UNKNOWN)
    realGpsLat = models.FloatField(default=0)
    realGpsLon = models.FloatField(default=0)
    estimatedGpsLat = models.FloatField(default=0)
    estimatedGpsLon = models.FloatField(default=0)
    estimatedAddressLat = models.FloatField(default=0)
    estimatedAddressLon = models.FloatField(default=0)
    estimatedAddress = models.CharField(max_length=150)
    targetAddress = models.CharField(max_length=150)
    recordTime = models.DateTimeField()
    success = models.BooleanField(default=False)
    fromMyTesting = models.BooleanField(default=False)

class GpsCoords(models.Model):
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class RecordedBeforeCorner(GpsCoords):
    pass

class RecordedAfterCorner(GpsCoords):
    pass