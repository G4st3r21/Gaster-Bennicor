import os
import sys
import pygame
import requests


api_server = "http://static-maps.yandex.ru/1.x/"
lon = "37.530887"
lat = "55.703118"
delta = "0.002"
step = 0.01
map_file = "map.png"

pygame.init()
screen = pygame.display.set_mode((600, 450))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                delta = str(float(delta) + step)
            elif event.key == pygame.K_PAGEUP:
                delta = str(float(delta) - step)

    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }
    
    response = requests.get(api_server, params=params)

    with open(map_file, "wb") as file:
        file.write(response.content)
    
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()

pygame.quit()
os.remove(map_file)
