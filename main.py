import os
import sys
import pygame
import requests
import argparse
import pygame_textinput
from itertools import cycle
from button import Button


# params 37.530887 55.703118 15
parser = argparse.ArgumentParser()
# Если аргументов нет, то выбираются по умолчанию
parser.add_argument("first_coord", nargs='?')
parser.add_argument("second_coord", nargs='?')
parser.add_argument("scale", nargs='?')
args = parser.parse_args()

pygame.init()
font = pygame.font.Font(None, 25)
textinput = pygame_textinput.TextInput()  # Объект textinput
clock = pygame.time.Clock()
textinput.text_color = (255, 255, 255)
textinput.antialias = False
map_file = "map.png"
maps = cycle(["map", "sat", "sat,skl"])
titles = cycle(["Схема", "Спутник", "Гибрид"])

api_server = "http://static-maps.yandex.ru/1.x/"

if args.scale is not None:
    lon = str(args.first_coord)
    lat = str(args.second_coord)
    z = int(args.scale)
else:
    lon = '37.530887'
    lat = '55.703118'
    z = '15'
l = next(maps)
mark_coords = lon, lat

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

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            new_coords = textinput.get_text()
            if event.key == pygame.K_PAGEDOWN and int(z) >= 1:
                z = str(int(z) - scale_step)
                changes_made = True
            elif event.key == pygame.K_PAGEUP and int(z) <= 21:
                z = str(int(z) + scale_step)
                changes_made = True
            elif event.key == pygame.K_TAB and new_coords:
                args = new_coords.split()
                if len(args) == 3:
                    lon = args[0]
                    lat = args[1]
                    z = args[2]
                    changes_made = True
                    textinput.clear_text()
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
        screen.fill((0, 0, 0))
        try:
            params = {
                "ll": ",".join([lon, lat]),
                "z": z,
                "l": l,
                "pt": f"{mark_coords[0]},{mark_coords[1]},pm2vvl"
            }
            response = requests.get(api_server, params=params)

            with open(map_file, "wb") as file:
                file.write(response.content)

            screen.blit(pygame.image.load(map_file), (0, 0))
        except Exception as E:
            print(E)

    # Работа строки ввода
    screen.blit(textinput.get_surface(), (150, 450))
    textinput.update(events)

    changes_made = False
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
os.remove(map_file)
