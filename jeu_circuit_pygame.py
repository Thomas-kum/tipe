import pygame
from pygame.locals import *
import math

pygame.init()
circuit_taille=(800, 600)
circuit_debut=(740,320)
ecran = pygame.display.set_mode(circuit_taille)

circuit_image = pygame.image.load("circuit.png")
circuit_image = pygame.transform.scale(circuit_image,circuit_taille)

class Voiture:
    def __init__(self,nom_fichier_image,debut,IA):
        # Données sur la voiture
        # Capacités de la voiture
        global voiture_acceleration_palier
        global voiture_freinage_palier
        global voiture_rotation_palier
        voiture_acceleration_palier=0.05 # Incrémentation de la vitesse à chaque clic (accélération).
        voiture_freinage_palier=0.1 # Incrémentation de la vitesse à chaque clic (freinage).
        voiture_rotation_palier = 3
        self.voiture_type=IA
        # Variables d'état
        self.x = debut[0]
        self.y = debut[1]
        self.vitesse = 0
        self.orientation = 0
        # Avancement de la voiture.
        self.nb_tours=0
        # Représentation de la voiture.
        self.car_image = pygame.image.load(nom_fichier_image)
        self.car_image = pygame.transform.scale(self.car_image, (30, 50))
        #self.car_image = pygame.transform.rotate(self.car_image, self.orientation)

    def rotation(self,gauche=False,droite=False):
        if gauche and self.vitesse!=0:
            self.orientation -= voiture_rotation_palier
        elif droite and self.vitesse!=0:
            self.orientation += voiture_rotation_palier

    def deplacement(self,acce=False,frei=False):
        if acce:
            self.vitesse += voiture_acceleration_palier
        elif frei and self.vitesse>0:
            self.vitesse -= voiture_freinage_palier

    def depart(self,debut):
        self.x=debut[0]
        self.y=debut[1]
        self.vitesse=0
        self.orientation=0
        self.nb_tours=0
 
    def update(self):
        self.orientation=self.orientation%360
        self.x += self.vitesse * math.sin(math.radians(self.orientation))
        self.y -= self.vitesse * math.cos(math.radians(self.orientation))
        if self.vitesse <0:
            self.vitesse=0

def jeu_deplacement(vehicule):
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        vehicule.rotation(gauche=True)
    if keys[K_RIGHT]:
        vehicule.rotation(droite=True)
    if keys[K_UP]:
        vehicule.deplacement(acce=True)
    if keys[K_DOWN]:
        vehicule.deplacement(frei=True)

def jeu_controles(vehicule):
    if not (0<=vehicule.x<=circuit_taille[0] and 0<=vehicule.y<=circuit_taille[1]):
        print("Sortie de cadre !")
        print(vehicule.x)
        vehicule.depart(circuit_debut)

    if circuit_image.get_at((int(vehicule.x), int(vehicule.y))) == (0, 0, 0):
        print("Echec -> Circuit !")
        print(vehicule.x,vehicule.y)
        vehicule.depart(circuit_debut)

def jeu_victoire(vehicule):
    if circuit_image.get_at((int(vehicule.x), int(vehicule.y))) == (76, 255, 0):
        vehicule.nb_tours+=1

def jeu_update(vehicule):
    rotated_car_image = pygame.transform.rotate(vehicule.car_image, -vehicule.orientation)
    car_rect = rotated_car_image.get_rect(center=(vehicule.x, vehicule.y))
    ecran.blit(rotated_car_image, car_rect)

def jeu(liste_vehicules):
    jeu_en_cours = True
    while jeu_en_cours:
        for event in pygame.event.get():
            if event.type == QUIT:
                jeu_en_cours = False

        for vehicule in liste_vehicules:
            if not(vehicule.voiture_type):
                jeu_deplacement(vehicule)

            vehicule.update()
            jeu_controles(vehicule)
            jeu_victoire(vehicule)

        ecran.blit(circuit_image, (0, 0))
        for vehicule in liste_vehicules:
            jeu_update(vehicule)
        pygame.display.update()
        pygame.time.Clock().tick(90)

    pygame.quit()

jeu([Voiture("voiture.png", circuit_debut,False)])
