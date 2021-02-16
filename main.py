import os
import sys
import pygame
import requests
import argparse
import pygame_textinput
from itertools import cycle
from button import Button
from geocode import request


# params 37.530887 55.703118 15
parser = argparse.ArgumentParser()
# Если аргументов нет, то выбираются по умолчанию
parser.add_argument("first_coord", nargs='?', default=37.530887)
parser.add_argument("second_coord", nargs='?', default=55.703118)
parser.add_argument("scale", nargs='?', default=15)
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

lon = str(args.first_coord)
lat = str(args.second_coord)
z = int(args.scale)
l = next(maps)
mark_coords = lon, lat

scale_step = 1
coords_step = 0.005

screen = pygame.display.set_mode((600, 500))
map_button = Button(screen, 0, 450, 150, 50, next(titles), font)
find_button = Button(screen, 450, 450, 150, 50, 'Поиск', font)
reset_button = Button(screen, 450, 0, 150, 50, 'Сброс', font)

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
            if event.key == pygame.K_PAGEDOWN and int(z) >= 1:
                z = str(int(z) - scale_step)
                changes_made = True
            elif event.key == pygame.K_PAGEUP and int(z) <= 21:
                z = str(int(z) + scale_step)
                changes_made = True
            elif event.key == pygame.K_UP:
                lat = str(float(lat) + coords_step)
                changes_made = True
            elif event.key == pygame.K_DOWN:
                lat = str(float(lat) - coords_step)
                changes_made = True
            elif event.key == pygame.K_LEFT:
                lon = str(float(lon) - coords_step)
                changes_made = True
            elif event.key == pygame.K_RIGHT:
                lon = str(float(lon) + coords_step)
                changes_made = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True

    x, y = pygame.mouse.get_pos()

    # Работа кнопок-----------------------------------------------
    if map_button.collide((x, y)) and click:
        map_button.set_text(next(titles))
        l = next(maps)
        changes_made = True
    if find_button.collide((x, y)) and click:
        arg = textinput.get_text()  # Получаем аргументы из строки
        if len(list(arg)) > 1:
            arg = arg.split()
        else:
            arg = list(arg)
        coords = request(arg).split()
        print(coords)
        if coords:  # Записываем их в переменные
            lon = coords[0]
            lat = coords[1]
            mark_coords = lon, lat
            changes_made = True
            textinput.clear_text()  # Очищаем строку
    if reset_button.collide((x, y)) and click:
        lon = str(args.first_coord)
        lat = str(args.second_coord)
        changes_made = True

    textinput.update(events)  # Обновление строки ввода

    if changes_made:
        # Если числа введены неверно, то прога не вылетает, а просто не выводит изображение
        try:
            print(z, l, lon, lat, mark_coords, sep='\n')
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
    screen.fill(pygame.Color("black"), (150, 450,
                                        screen.get_width(), screen.get_height()))
    screen.blit(textinput.get_surface(), (150, 450))

    # Обновление кнопок
    map_button.update()
    find_button.update()
    reset_button.update()

    changes_made = False
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
os.remove(map_file)
