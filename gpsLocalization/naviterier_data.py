import json

import requests


def getData(lat, lon, radius):
    url = "http://147.32.81.71/NaviTerier.ProcessingService/json/reply/FindSourceData"
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


def getSegments(lat, lon, radius, formOfWay ='All'):
    # collect all Naviterier data
    data = getData(lat, lon, radius)
    # skip others than segments
    segments = data['Segments']
    # filter by FormOfWay
    if formOfWay == 'All':
        return segments
    else:
        return _filterByFormOfWay(segments, formOfWay)


def _filterByFormOfWay(segments, formOfWay):
        sidewalks = []
        for element in segments:
            if element['FormOfWay'] == formOfWay:
                sidewalks.append(element)
        return sidewalks