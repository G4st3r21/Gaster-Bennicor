import os
import sys
import pygame
import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("first_coord")
parser.add_argument("second_coord")
parser.add_argument("scale")
args = parser.parse_args()

# params 37.530887 55.703118 15
map_file = "map.png"
api_server = "http://static-maps.yandex.ru/1.x/"
lon = str(args.first_coord)
lat = str(args.second_coord)
z = int(args.scale)
scale_step = 1
coords_step = 0.005

pygame.init()
screen = pygame.display.set_mode((600, 450))
running = True

while running:
    pressed_key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN and z >= 1:
                z -= scale_step
            elif event.key == pygame.K_PAGEUP and z <= 21:
                z += scale_step

    if pressed_key[pygame.K_UP]:
        lat = str(float(lat) + coords_step)
    if pressed_key[pygame.K_DOWN]:
        lat = str(float(lat) - coords_step)
    if pressed_key[pygame.K_LEFT]:
        lon = str(float(lon) - coords_step)
    if pressed_key[pygame.K_RIGHT]:
        lon = str(float(lon) + coords_step)

    params = {
        "ll": ",".join([lon, lat]),
        "z": z,
        "l": "map"
    }

    response = requests.get(api_server, params=params)

    with open(map_file, "wb") as file:
        file.write(response.content)
    
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()

os.remove(map_file)
