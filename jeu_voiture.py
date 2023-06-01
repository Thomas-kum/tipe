import pygame
from pygame.locals import *
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))

car_x_debut=740
car_y_debut=320
car_acceleration=0.05
car_freinage=0.1

nb_tours=0

car_x = car_x_debut
car_y = car_y_debut
car_speed = 0
car_angle = 0
car_rotation = 3

car_image = pygame.image.load("voiture.png")
car_image = pygame.transform.scale(car_image, (30, 50))
car_image = pygame.transform.rotate(car_image, car_angle)

circuit_image = pygame.image.load("circuit.png")
circuit_image = pygame.transform.scale(circuit_image, (800, 600))

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and car_speed!=0:
        car_angle -= car_rotation
    if keys[K_RIGHT] and car_speed!=0:
        car_angle += car_rotation
    if keys[K_UP]:
        car_speed += car_acceleration
    if keys[K_DOWN] and car_speed>0:
        car_speed -= car_freinage

    car_angle=car_angle%360
    
    car_x += car_speed * math.sin(math.radians(car_angle))
    car_y -= car_speed * math.cos(math.radians(car_angle))

    if car_speed <0:
        car_speed=0

    if not (5<=car_x<=795 and 5<=car_y<=595):
        print("")
        ValueError: print("Sortie de cadre !")
        print(car_rect)
        car_x = car_x_debut
        car_y = car_y_debut
        car_speed = 0
        car_angle = 0

    car_rect = car_image.get_rect(center=(car_x, car_y))
    #if circuit_image.get_at((car_rect.x, car_rect.y)) == (0, 0, 0):
    if circuit_image.get_at((int(car_x), int(car_y))) == (0, 0, 0):

        print("")
        print("Echec -> Circuit !")
        print(car_rect)
        print(car_x,car_y)
        car_x = car_x_debut
        car_y = car_y_debut
        car_speed = 0
        car_angle = 0
        print("Tours : ",nb_tours)
        nb_tours=0
    
    if circuit_image.get_at((int(car_x), int(car_y))) == (76, 255, 0):
        nb_tours+=1


    screen.blit(circuit_image, (0, 0))
    rotated_car_image = pygame.transform.rotate(car_image, -car_angle)
    car_rect = rotated_car_image.get_rect(center=(car_x, car_y))
    screen.blit(rotated_car_image, car_rect)

    pygame.display.update()
    pygame.time.Clock().tick(90)

print(nb_tours)
pygame.quit()
