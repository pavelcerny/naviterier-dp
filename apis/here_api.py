import json

import requests

from naviterier.views import simplifyHouseNumber

HERE_APP_ID = 'JuqrHIoriI7bnBIrWekn'
HERE_APP_CODE = 'YYFjqdWAc-CRWioPKT6Hog'


def getAddress(lat, lon):
    URL = "https://reverse.geocoder.cit.api.here.com/6.2/reversegeocode.json"
    # request here API
    payload = {
        "prox": str(lat) + ',' + str(lon) + ',' + '100',
        "mode": 'retrieveAddresses',
        "maxresults": '1',
        "gen": '8',
        "app_id": HERE_APP_ID,
        "app_code": HERE_APP_CODE,
    }
    url = URL
    r = requests.get(url, params=payload)
    data = r.text
    # parse json data
    data = json.loads(data)

    address = data['Response']['View'][0]['Result'][0]['Location']['Address']
    house_number = address['HouseNumber']
    street = address['Street']

    response_address = address = '{} {}'.format(street, simplifyHouseNumber(house_number))

    return response_address


