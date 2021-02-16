import requests


def get_coords(args):
    response = requests.get(
        'https://geocode-maps.yandex.ru/1.x/'
        '?apikey=40d1649f-0493-4b70-98ba-98533de7710b&'
        f'geocode={"+".join(args.split())}&format=json')

    response = response.json()

    coords = response['response']['GeoObjectCollection']['featureMember'][0]
    coords = coords['GeoObject']['Point']['pos']
    return coords


def get_address(args):
    response = requests.get(
        'https://geocode-maps.yandex.ru/1.x/'
        '?apikey=40d1649f-0493-4b70-98ba-98533de7710b&'
        f'geocode={"+".join(args.split())}&format=json')

    response = response.json()

    address = response['response']['GeoObjectCollection']['featureMember'][0]
    address = address["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
    return address
