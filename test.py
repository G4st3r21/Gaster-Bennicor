import requests


api_server = "http://static-maps.yandex.ru/1.x/"

params = {
    "ll": ",".join([lon, lat]),
    "z": z,
    "l": l,
    "pt": f"{mark_coords[0]},{mark_coords[1]},pm2vvl"
}
response = requests.get(api_server, params=params)

