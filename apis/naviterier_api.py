import json

import requests

# NAVITERIER_SERVER = "http://147.32.81.71/NaviTerier.ProcessingService"
# NAVITERIER_URL = NAVITERIER_SERVER + "/json/reply"
NAVITERIER_SERVER = "http://147.32.81.71/NaviTerier.ProcessingService"
NAVITERIER_URL = NAVITERIER_SERVER + "/json/reply"

def findSourceData(lat, lon, radius):
    """ find which data for given area are in the database """

    url = NAVITERIER_URL + "/FindSourceData"
    payload = {
        'SearchOrigin': {
            'Latitude': lat,
            'Longitude': lon
        },
        'Radius': radius,
    }
    headers = {'content-type': 'application/json'}

    serialized_data = json.dumps(payload)
    # request naviterier api
    r = requests.post(url, data = serialized_data)
    data = r.json()

    return data


def findSegments(lat, lon, radius, formOfWay ='All'):
    # collect all Naviterier data
    data = findSourceData(lat, lon, radius)
    # skip others than segments
    segments = data['Segments']
    # filter by FormOfWay
    if formOfWay == 'All':
        return segments
    else:
        return _filterByFormOfWay(segments, formOfWay)


def findRoutes(SourceAddress,TargetAddress):
    """ return all possible routes from SourceAddress to TargetAddress"""

    url = NAVITERIER_URL + "/FindRoutes"

    payload = {
        # "SourceAddressId": "21700851",
        # "SourcePoiId":"String",
        "SourceTextInput": SourceAddress,
        # "TargetAddressId": "21702519",
        # "TargetPoiId":"String",
        "TargetTextInput": TargetAddress,
    }
    headers = {'content-type': 'application/json',
               'Accept-Language': 'cs'}

    serialized_data = json.dumps(payload)
    # request naviterier api
    r = requests.post(url, data=serialized_data, headers=headers)
    data = r.json()

    return data


def getAddresses():
    """ return json with all addresses in naviterier database"""
    url = NAVITERIER_URL + "/GetAddresses"
    payload = {}
    headers = {'content-type': 'application/json'}

    serialized_data = json.dumps(payload)
    # request naviterier api
    r = requests.post(url, data = serialized_data, headers=headers)
    data = r.json()

    return data



def _filterByFormOfWay(segments, formOfWay):
        sidewalks = []
        for element in segments:
            if element['FormOfWay'] == formOfWay:
                sidewalks.append(element)
        return sidewalks


def getItinerary(sourceAddress, TargetAddress):
    response = findRoutes(sourceAddress, TargetAddress)
    response = _getFirstItinerary(response)

    return response


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


