import os
import sys

import pygame
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("first_coord", nargs='*')
parser.add_argument("second_coord", nargs='*')
parser.add_argument("delta", nargs='*')
args = parser.parse_args()

api_server = "http://static-maps.yandex.ru/1.x/"

# lon = "37.530887"
# lat = "55.703118"
# delta = "0.002"

lon = args.first_coord
lat = args.second_coord
delta = args.delta


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
    
    pressed_key = pygame.key.get_pressed()
    if pressed_key[pygame.K_UP]:
        lon += 0.005
    if pressed_key[pygame.K_DOWN]:
        lon -= 0.005
    if pressed_key[pygame.K_LEFT]:
        lat += 0.005
    if pressed_key[pygame.K_RIGHT]:
        lat -= 0.005

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()

os.remove(map_file)
