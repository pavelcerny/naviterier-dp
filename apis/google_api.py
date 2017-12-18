import json

import requests


# for Google API https://developers.google.com/maps/documentation/


# credentials
GOOGLE_API_KEY = "AIzaSyC7WCaTEPswl2Cs77ncqxiz7O4fLK2z2Wk"
URL = "https://maps.googleapis.com/maps/api/geocode/json"


def getAddress(lat, lon):
    """
    Returns Address for given latitude and longitude. The format of the address 'streetName houseNumber'

    >>>getAddress(50.0777201, 14.416807)
    'Myslíkova 13'
    """

    # request google API
    payload = {'latlng': str(lat) + "," + str(lon),  # 50.094265,
               'key': GOOGLE_API_KEY}
    url = URL
    r = requests.get(url, params=payload)
    data = r.text
    # parse json data
    data = json.loads(data)

    # first result uses to be correct
    first = data['results'][0]['address_components']

    street = first[2]['long_name']
    number =  first[0]['long_name']
    premise =  first[1]['long_name']
    # address = '{} {}/{}'.format(street, premise, number)
    address = '{} {}'.format(street, number)

    return address


def getGps(address):
    """
    Returns lat & lon for given address.

    >>>getGPS('Myslíkova 187/13')
    {'lat' : 50.0777201, 'lon' : 14.416807}
    >>>getGPS('Myslíkova 13')
    {'lat' : 50.0777201, 'lon' : 14.416807}
    """

    # request google API
    payload = {'address': address}
    url = URL
    r = requests.get(url, params=payload)
    data = r.text
    
    # EXAMPLE RESPONSE
    #     {
    #     "results": [
    #         {
    #             "address_components": [
    #                 ...
    #             ],
    #             "formatted_address": "Karlovo nám. 319/3, Nové Město, 120 00 Praha-Praha 2, Czechia",
    #             "geometry": {
    #                 "location": {
    #                     "lat": 50.0739567,
    #                     "lng": 14.4185332
    #                 },
    #                 ...
    #             },
    #             ...
    #         }
    #     ],
    #     "status": "OK"
    # }

    # parse json data
    data = json.loads(data)
    # get object with "lat" and "lng"
    location = data['results'][0]['geometry']['location']

    response = {
        "lat": location["lat"],
        "lon": location["lng"],
    }
    return response