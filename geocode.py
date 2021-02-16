import requests


def request(args):
    response = requests.get(
        'https://geocode-maps.yandex.ru/1.x/'
        '?apikey=40d1649f-0493-4b70-98ba-98533de7710b&'
        f'geocode={"+".join(args)}&format=json')

    response = response.json()

    coords = response['response']['GeoObjectCollection']['featureMember'][0]
    coords = coords['GeoObject']['Point']['pos']
    return coords
