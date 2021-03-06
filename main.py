import os
import sys
import pygame
import requests
import argparse
import pygame_textinput
from itertools import cycle
from button import Button
from geocode import get_coords, get_address


parser = argparse.ArgumentParser()
# Если аргументов нет, то выбираются по умолчанию
parser.add_argument("first_coord", nargs='?', default=37.530887)
parser.add_argument("second_coord", nargs='?', default=55.703118)
parser.add_argument("scale", nargs='?', default=15)
args = parser.parse_args()

pygame.init()
font = pygame.font.Font(None, 25)  # Основной шрифт
address_font = pygame.font.Font(None, 20)  # Шрифт для вывода адреса

clock = pygame.time.Clock()
textinput = pygame_textinput.TextInput(
    cursor_color=(255, 255, 255))  # Объект textinput
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
address = get_address(lon + " " + lat)

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

    # Обработка нажатий на кнопки
    if map_button.collide((x, y)) and click:
        map_button.set_text(next(titles))
        l = next(maps)
        changes_made = True

    if find_button.collide((x, y)) and click:
        arg = textinput.get_text()  # Получаем введенный адрес
        coords = get_coords(arg)
        address = get_address(coords)

        if coords:  # Записываем их в переменные
            lon, lat = coords.split()
            mark_coords = lon, lat
            changes_made = True
            textinput.clear_text()  # Очищаем строку

    if reset_button.collide((x, y)) and click:  # Обнуляем все переменные
        lon = str(args.first_coord)
        lat = str(args.second_coord)
        z = int(args.scale)
        mark_coords = lon, lat
        address = get_address(lon + " " + lat)
        changes_made = True

    textinput.update(events)  # Обновление строки ввода

    if changes_made:
        # Если числа введены неверно, то прога не вылетает, а просто не выводит изображение
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
    screen.fill(pygame.Color("black"), (150, 450,
                                        screen.get_width(), screen.get_height()))
    screen.blit(textinput.get_surface(), (150, 450))

    # Вывод адреса обьекта
    screen.fill(pygame.Color("black"), (0, 0, 500, 50))
    # Вставить переменную с настоящим адресом
    if len(address) < 50:
        text1 = address_font.render(address, 1, pygame.Color("white"))
        text2 = address_font.render('', 1, pygame.Color("white"))
    else:
        text1 = address_font.render(address[:50], 1, pygame.Color("white"))
        text2 = address_font.render(address[50:], 1, pygame.Color("white"))
    text_rect1 = text1.get_rect()
    text_rect1.center = (500 * 0.5, 30 * 0.5)
    text_rect2 = text2.get_rect()
    text_rect2.center = (500 * 0.5, 60 * 0.5)
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)

    # Обновление кнопок
    map_button.update()
    find_button.update()
    reset_button.update()

    changes_made = False
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
os.remove(map_file)
