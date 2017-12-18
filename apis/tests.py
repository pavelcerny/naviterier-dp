from django.test import TestCase

from apis import naviterier_api
from apis import google_api



class GoogleApiTests(TestCase):
    def test_gps_to_address(self):
        lat = 50.0777201
        lon = 14.416807
        should_be = "Myslíkova 13"
        self.assertEqual(google_api.getAddress(lat, lon),should_be)

    def test_address_to_gps(self):
        address = "Myslíkova 187/13"
        should_be = {
            'lat' : 50.0777201,
            'lon' : 14.416807
        }
        self.assertEqual(google_api.getGps(address), should_be)

    def test_address_to_gps(self):
        address = "Myslíkova 13"
        should_be = {
            'lat' : 50.0777201,
            'lon' : 14.416807
        }
        self.assertEqual(google_api.getGps(address), should_be)

class NaviterierApiTests(TestCase):
    def test_get_itinerary(self):
        sourceAddress = "Myslíkova 13"
        targetAddress = "Vodičkova 2"

        itinerary = naviterier_api.getItinerary(sourceAddress,targetAddress)

        self.assertEqual( "GeneralDescription" in itinerary, True)


class WatsonApiTests(TestCase):
    pass
