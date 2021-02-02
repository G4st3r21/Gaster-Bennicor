import os
import sys

import pygame
import requests

api_server = "http://static-maps.yandex.ru/1.x/"

lon = "37.530887"
lat = "55.703118"
delta = "0.002"

params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
    "l": "map"
}

pygame.init()
screen = pygame.display.set_mode((600, 450))

while pygame.event.wait().type != pygame.QUIT:
    response = requests.get(api_server, params=params)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
        print(1)
    
    pressed = pygame.key.get_pressed
    
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()

os.remove(map_file)
