import json

import requests

NAVITERIER_SERVER = "http://147.32.81.71/NaviTerier.ProcessingService"
NAVITERIER_URL = NAVITERIER_SERVER + "/json/reply"


def findSourceData(lat, lon, radius):
    """
    Find all data in the database in given radius around the given area.

    :returns:
    i.e.
    >>>findSourceData(50.0777201, 14.416807, 50)
    {dict} {'Addresses': [], 'AddressEntryPoints': [], 'CrossWays': [], 'Segments':[], 'Pois':[], 'PoiEntryPoints':[]}
    """

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
    """
    Find all Segments in the database in given radius around the given area.
    Segment can be: Sidewalk, WalkWay, Crossway, 3, 20, ...

    :param formOfWay: allows filtering by the type of the segment
    i.e.
    >>>findSegments(lat, lon, radius)
    all segments

    >>>findSegments(lat, lon, radius, 'Walkable')
    only Sidewalks + Walkways

    >>>findSegments(lat, lon, radius, 'FilteredType')
    only FilteredType

    :returns: list of segments of desired type
    i.e.
    <class 'list'>: [
        {'Id': '278477', 'Name': 'Magdalény Rettigové',
         'Shape': {'Points': [{'Latitude': 50.0791625472122, 'Longitude': 14.420189734626}, {'Latitude': 50.0799457146606, 'Longitude': 14.4202691600481}]},
         'FormOfWay': '3'
        },
        {...},
        {...},
        ]
    """

    # collect all Naviterier data
    data = findSourceData(lat, lon, radius)
    # skip others than segments
    segments = data['Segments']
    # filter by FormOfWay
    if formOfWay == 'All':
        return segments
    elif formOfWay == "Walkable":
        sidewalks = _filterByFormOfWay(segments, "Sidewalk")
        # enter all possible FormOfWay you want to use i.e. WalkWay, Crossway, etc.:
        # ie. walkways = _filterByFormOfWay(segments, "WalkWay")
        # unite them:
        # i.e. filtered_segments = sidewalks + walkways
        filtered_segments = sidewalks
        return filtered_segments
    else:
        return _filterByFormOfWay(segments, formOfWay)


def findRoutes(SourceAddress,TargetAddress):
    """
    Return all possible routes from SourceAddress to TargetAddress

    :returns:
    i.e.
    {dict} {'Routes': [ {'Shape': {'Points': [{'Latitude': 50.0792356153877, 'Longitude': 14.4204030439143},
                                                {'Latitude': 50.0792396869288, 'Longitude': 14.4202555808499}, ...]},
                         'Itinerary': {'GeneralDescription': 'Trasa z adresy Lazarská 1718/3 na adresu Myslíkova 187/13. Trasa je asi 380 metrů dlouhá a vede přes 4 přechody. Postav se tak, abys měl budovy za zády.',
                         'Stages': ['1. úsek z 12. \r\nNacházíš se na adrese Lazarská 1718/3. \r\nOtoč se vpravo a jdi asi 10 metrů mírně z kopce na roh s ulicí Magdalény Rettigové. Po pravé ruce měj budovy.', '2. úsek z 12. \r\nNacházíš se na rohu ulic Lazarská a Magdalény Rettigové. \r\nPokračuj vpřed a přejdi ulici Magdalény Rettigové na protější roh přes značený přechod s obousměrným provozem.', '3. úsek z 12. \r\nNacházíš se na rohu ulic Lazarská a Magdalény Rettigové. \r\nPokračuj vpřed a jdi asi 30 metrů na zkosený roh s ulicí Spálená. Po pravé ruce měj budovy.', '4. úsek z 12. \r\nNacházíš se na zkoseném rohu ulic Lazarská a Spálená. \r\nOdboč mírně vpravo a jdi pár metrů k přechodu po levé ruce. Po pravé ruce měj budovy.', '5. úsek z 12. \r\nNacházíš se u přechodu přes ulici Spálená. \r\nOtoč se mírně vlevo a přejdi ulici Spálená na protější chodník přes značený přechod s jednosměrným provozem zprava a tramvají.', '6. úsek z 12. \r\nNacházíš se v ulici Spálená. \r\nOtoč se vlevo a jdi asi 90 metrů na roh s ulicí Myslíkova. Po pravé ruce měj budovy.', '7. úsek z 12. \r\nNacházíš se na rohu ulic Spálená a Myslíkova. \r\nOdboč vpravo a jdi asi 40 metrů k přechodu. Po pravé ruce měj budovy.', '8. úsek z 12. \r\nNacházíš se u přechodu přes ulici Černá. \r\nPokračuj vpřed a přejdi ulici Černá na protější chodník přes značený přechod s jednosměrným provozem zleva.', '9. úsek z 12. \r\nNacházíš se v ulici Myslíkova. \r\nPokračuj vpřed a jdi asi 80 metrů na roh s ulicí Myslíkova. Po pravé ruce měj budovy.', '10. úsek z 12. \r\nNacházíš se na rohu ulic Myslíkova a Křemencova. \r\nPokračuj vpřed a přejdi ulici Křemencova na protější roh přes značený přechod s jednosměrným provozem zprava.', '11. úsek z 12. \r\nNacházíš se na zkoseném rohu ulic Myslíkova a Křemencova. \r\nPokračuj vpřed a jdi asi 80 metrů mírně z kopce na adresu Myslíkova 187/13 po pravé ruce. Po pravé ruce měj budovy.', '12. úsek z 12. \r\nJsi v cíli. Nacházíš se na adrese Myslíkova 187/13. \r']}}],
                         'SourceAddress': {'Id': '21713685', 'Shape': {'Latitude': 50.0792751119734, 'Longitude': 14.4204056768158}, 'Street': 'Lazarská', 'HouseNumber': '3', 'LandRegistryNumber': '1718', 'City': 'Praha'},
                         'TargetAddress': {'Id': '21702713', 'Shape': {'Latitude': 50.0777158608146, 'Longitude': 14.4166350421216}, 'Street': 'Myslíkova', 'HouseNumber': '13', 'LandRegistryNumber': '187', 'City': 'Praha'},
                         'MapVersion': '2017-01-16.gdb'},
                         {...},
                         {...}]
            }
    """

    url = NAVITERIER_URL + "/FindRoutes"

    payload = {
        # "SourceAddressId": "21713685",
        # "SourcePoiId": "60049515",
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
    """
    Return dictionary with all addresses in the naviterier database

    :returns
    i.e.
    {'Addresses': [{'Id': '40825124',
                    'Shape': {'Latitude': 50.0887841946588, 'Longitude': 14.4442259626852},
                    'Street': 'Pernerova',
                    'HouseNumber': '2b',
                    'LandRegistryNumber': '2870',
                    'City': 'Praha'},
                   {...},
                   {...}]
    }
    """
    url = NAVITERIER_URL + "/GetAddresses"
    payload = {}
    headers = {'content-type': 'application/json'}

    serialized_data = json.dumps(payload)
    # request naviterier api
    r = requests.post(url, data = serialized_data, headers=headers)
    data = r.json()

    return data



def _filterByFormOfWay(segments, formOfWay):
    """
    Creates a new array of Segments, which contains the elements of segments, which are the given FormOfWay
    :param segments:  [{...}, {...}, ...]
    :return: [{...},{...},...]
    """
    sidewalks = []
    for element in segments:
        if element['FormOfWay'] == formOfWay:
            sidewalks.append(element)
    return sidewalks


def getItinerary(sourceAddress, targetAddress):
    '''
    Get route's itinerary between sourceAddress and TargetAddress
    :param sourceAddress: String in format 'FromStreet houseNumber'
    :param targetAddress: String in format 'ToStreet houseNumber'
    :returns: description and stages of the path
    i.e.
    {dict}{'GeneralDescription': 'Trasa z adresy Lazarská 1718/3 na adresu Myslíkova 187/13. Trasa je asi 380 metrů dlouhá a vede přes 4 přechody. Postav se tak, abys měl budovy za zády.',
           'Stages': ['1. úsek z 12. \r\nNacházíš se na adrese Lazarská 1718/3. \r\nOtoč se vpravo a jdi asi 10 metrů mírně z kopce na roh s ulicí Magdalény Rettigové. Po pravé ruce měj budovy.',
                      '2. úsek z 12. \r\nNacházíš se na rohu ulic Lazarská a Magdalény Rettigové. \r\nPokračuj vpřed a přejdi ulici Magdalény Rettigové na protější roh přes značený přechod s obousměrným provozem.',
                      ...,
                      '12. úsek z 12. \r\nJsi v cíli. Nacházíš se na adrese Myslíkova 187/13. \r'
                      ]}
    '''

    response = findRoutes(sourceAddress, targetAddress)
    # take the first result (there can be more results)



    response = _getFirstItinerary(response)
    targetRecognized = True
    sourceRecognized = True

    if "TargetAddress" not in response:
        targetRecognized = False
    if "SourceAddress" not in response:
        sourceRecognized = False

    sourceInDB = True
    targetInDB = True

    if not targetRecognized:
        targetInDB = _isInDB(targetAddress)
    if not sourceRecognized:
        targetInDB = _isInDB(targetAddress)

    #TODO return why address is not recognized

    return response


def _isInDB(address):
    #TODO valiate the presence in the Naviterier DB of Addresses
    pass


def _getFirstItinerary(response):
    """
    Returns the first Itinerary on the list from Response of Naviterier routing server response.

    :param response: the response from NAVITERIER/json/metadata?op=FindRoutes
    i.e.
    {'Routes': [{'Shape': {'Points': [{...},{...},{...}]}}],
                 'SourceAddress': {...},
                 'TargetAddress': {...},
                 'MapVersion': '...'],
               [...],
               [...]
    }

    :returns the first itinerary GeneralDescriptions & Stages
    i.e.
    {'GeneralDescription': 'Trasa z adresy Lazarská 1718/3 na adresu Myslíkova 187/13. Trasa je asi 380 metrů dlouhá a vede přes 4 přechody. Postav se tak, abys měl budovy za zády.',
     'Stages': ['1. úsek z 12. \r\nNacházíš se na adrese Lazarská 1718/3. \r\nOtoč se vpravo a jdi asi 10 metrů mírně z kopce na roh s ulicí Magdalény Rettigové. Po pravé ruce měj budovy.',
                ...,
               ]
    }
    """

    # check if the Target and Source Address were recognized by the Naviterier server

    if "TargetAddress" not in response:
        if "SourceAddress" not in response:
            return generateErrorItinerary("Target address and Source address are wrongly written. Double check they are correct")
        else:
            return generateErrorItinerary("Target address is wrongly written. Double check it's correct")
    if "SourceAddress" not in response:
        return generateErrorItinerary("Source address is wrongly written. Double check it's correct")

    # return the first variant(response can contain more variants)
    itinerary = response["Routes"][0]["Itinerary"]
    return itinerary


def generateErrorItinerary(message):
    eItinerary = {'GeneralDescription': message,
                  'Stages': []
                 }
    return eItinerary


