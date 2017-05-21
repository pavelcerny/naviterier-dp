import json

from django.shortcuts import render, HttpResponse
from unidecode import unidecode

# Create your views here.
from apis.naviterier_api import getAddresses
from naviterier.models import Address, Shape


def updateAddressesDbAPI(request):
    addresses = getAddresses()
    addresses = addresses['Addresses']

    # delete old
    Address.objects.all().delete()

    # store new
    for a in addresses:
        aToStore = Address()
        aToStore.id = a['Id']
        shape = Shape()
        shape.latitude = a["Shape"]["Latitude"]
        shape.longitude = a["Shape"]["Longitude"]
        aToStore.shape = shape
        aToStore.street = a["Street"]
        aToStore.street_noaccents = simplify(a["Street"])
        aToStore.houseNumber = a["HouseNumber"]
        aToStore.landRegistryNumber = a["LandRegistryNumber"]
        aToStore.city = a["City"]

        aToStore.save()

    return HttpResponse("addresses updated")


def isAddressInDbAPI(request):
    address = request.GET['address']
    words = address.split(None)
    street = ""
    i=0
    for w in words[0:-1]:
        if i!=0:
            street += " "
        street += w
    if len(words) < 2:
        number = 'prázdné'
    else:
        number = words[-1]
    response = json.dumps(isAddressInDB(street,number))
    return HttpResponse(response, content_type='application/json')





def isAddressInDB(street, house_number):
    """ 
    return dictionary
    street: True/False
    streetAndHouseNumber: True/False
    streetAndLandRegistryNumber: True/False
    input: street
            number
            
    """
    street_noaccents = simplify(street)

    house_number_simplified = simplifyHouseNumber(house_number)

    count_house_number = Address.objects.filter(street_noaccents=street_noaccents,
                                                houseNumber=house_number_simplified).count()
    count_landRegistryNumber = Address.objects.filter(street_noaccents=street_noaccents,
                                                      landRegistryNumber=house_number_simplified).count()

    if count_house_number > 0 or count_landRegistryNumber > 0:
        count_street = 1;
    else:
        count_street = Address.objects.filter(street_noaccents=street_noaccents).count()

    response = {
        "street": True if count_street > 0 else False,
        "streetAndHouseNumber": True if count_house_number > 0 else False,
        "streetAndLandRegistryNumber": True if count_landRegistryNumber > 0 else False,
        "input" : {
            "street":street,
            "number":house_number_simplified,
        }
    }

    return response


def simplify(text):
    """ Remove diacritics and put to small letters
    i.e. Čauky ---> cauky"""
    s = unidecode(u'' + text).lower()
    only_letters = ''.join(filter(str.isalpha, s))
    return only_letters


def simplifyHouseNumber(number):
    if "/" in number:
        landRegistryNumber, houseNumber = number.split("/", 1)
        return houseNumber
    else:
        return number
