import pygame
from pygame.locals import *
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))

car_x = 550
car_y = 300
car_speed = 0
car_angle = -90

car_image = pygame.image.load("voiture.png")
car_image = pygame.transform.scale(car_image, (50, 50))

circuit_image = pygame.image.load("circuit.png")
circuit_image = pygame.transform.scale(circuit_image, (800, 600))

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        car_angle -= 5
    if keys[K_RIGHT]:
        car_angle += 5
    if keys[K_UP]:
        car_speed += 0.1
    if keys[K_DOWN]:
        car_speed -= 0.1

    car_x += car_speed * math.cos(math.radians(car_angle))
    car_y += car_speed * math.sin(math.radians(car_angle))

    car_rect = car_image.get_rect(center=(car_x, car_y))
    if circuit_image.get_at((car_rect.x, car_rect.y)) == (0, 0, 0):
        print("Echec -> Remise à zéro !")
        print(car_rect)
        car_x = 550
        car_y = 300
        car_speed = 0
        car_angle = -90

    screen.blit(circuit_image, (0, 0))
    rotated_car_image = pygame.transform.rotate(car_image, car_angle)
    car_rect = rotated_car_image.get_rect(center=(car_x, car_y))
    screen.blit(rotated_car_image, car_rect)

    pygame.display.update()
    pygame.time.Clock().tick(60)

pygame.quit()