import os
import sys
import pygame
import requests
import argparse
from itertools import cycle
from button import Button


parser = argparse.ArgumentParser()
parser.add_argument("first_coord")
parser.add_argument("second_coord")
parser.add_argument("scale")
args = parser.parse_args()

# params 37.530887 55.703118 15
pygame.init()
font = pygame.font.Font(None, 25)
map_file = "map.png"
maps = cycle(["map", "sat", "sat,skl"])
titles = cycle(["Схема", "Спутник", "Гибрид"])

api_server = "http://static-maps.yandex.ru/1.x/"
lon = str(args.first_coord)
lat = str(args.second_coord)
z = int(args.scale)
l = next(maps)

scale_step = 1
coords_step = 0.005

screen = pygame.display.set_mode((600, 500))
map_button = Button(screen, 0, 450, 150, 50, next(titles), font)

click = False
changes_made = True
running = True

while running:
    pressed_key = pygame.key.get_pressed()
    click = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN and z >= 1:
                z -= scale_step
                changes_made = True
            elif event.key == pygame.K_PAGEUP and z <= 21:
                z += scale_step
                changes_made = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                click = False

    if pressed_key[pygame.K_UP]:
        lat = str(float(lat) + coords_step)
        changes_made = True
    if pressed_key[pygame.K_DOWN]:
        lat = str(float(lat) - coords_step)
        changes_made = True
    if pressed_key[pygame.K_LEFT]:
        lon = str(float(lon) - coords_step)
        changes_made = True
    if pressed_key[pygame.K_RIGHT]:
        lon = str(float(lon) + coords_step)
        changes_made = True

    map_button.update()

    x, y = pygame.mouse.get_pos()
    if map_button.collide((x, y)) and click:
        map_button.set_text(next(titles))
        l = next(maps)
        changes_made = True

    if changes_made:
        params = {
            "ll": ",".join([lon, lat]),
            "z": z,
            "l": l
        }

        response = requests.get(api_server, params=params)

        with open(map_file, "wb") as file:
            file.write(response.content)
    
        screen.blit(pygame.image.load(map_file), (0, 0))
        
    changes_made = False
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
