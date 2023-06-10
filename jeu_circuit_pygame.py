import pygame
from pygame.locals import *
import math
import time
from annexe import *

pygame.init()
circuit_taille=(2000, 1000)
circuit_debut=(1890,440)
ecran = pygame.display.set_mode(circuit_taille)

circuit_image = pygame.image.load("circuit.png")
circuit_image = pygame.transform.scale(circuit_image,circuit_taille)

class Voiture:
    def __init__(self,nom_fichier_image,debut,IA):
        # Données sur la voiture
        global taille_voiture
        taille_voiture=(30,50)
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
        self.avancement_tour=0
        self.tours=[] # Permet de stocker les temps au tour de chaque voiture.
        # Représentation de la voiture.
        self.car_image = pygame.image.load(nom_fichier_image)
        self.car_image = pygame.transform.scale(self.car_image, taille_voiture)
        # Informations de chronométrage.
        self.temps_debut=time.time()

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
        self.avancement_tour=0
        self.temps_debut=time.time()
        self.vitesse=0
        self.orientation=0
        self.nb_tours=0
 
    def update(self):
        self.orientation=self.orientation%360
        self.x += self.vitesse * math.sin(math.radians(self.orientation))
        self.y -= self.vitesse * math.cos(math.radians(self.orientation))
        if self.vitesse <0:
            self.vitesse=0

    def chronometre(self):
        tempscomplet=time.time() - self.temps_debut
        self.tours.append(tempscomplet)
        return tempscomplet
    
    def radar(self):
        pas=3
        longueur_max=250
        angles=[-60,-30,0,30,60]
        donnees=[]
        for valeur_angle in angles:
            longueur=taille_voiture[1]/2
            test=True
            while test:
                angle_teste=self.orientation+math.radians(valeur_angle)-math.pi/2
                x_1,y_1=transformation((self.x,self.y),longueur,angle_teste)
                if circuit_image.get_at((x_1, y_1)) == (0, 0, 0):
                    test=False
                    donnees.append(longueur)
                elif longueur> longueur_max:
                    test=False
                    donnees.append(float("infinity"))
                else:
                    longueur+=pas
        return donnees



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

    if circuit_image.get_at((int(vehicule.x), int(vehicule.y))) == (0, 0, 255):
        print("Fin du tour.")
        vehicule.depart(circuit_debut)

def jeu_tour(vehicule):
    if circuit_image.get_at((int(vehicule.x), int(vehicule.y))) == (0, 255, 0) and vehicule.avancement_tour==3:
        vehicule.chronometre()
    elif circuit_image.get_at((int(vehicule.x), int(vehicule.y))) == (255, 0, 0):
        vehicule.avancement_tour+=1
    
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
            vehicule.radar()
            jeu_controles(vehicule)
            jeu_tour(vehicule)

        ecran.blit(circuit_image, (0, 0))
        for vehicule in liste_vehicules:
            jeu_update(vehicule)
        pygame.display.update()
        pygame.time.Clock().tick(90)

    for vehicule in liste_vehicules:
        print(vehicule.tours)
    pygame.quit()

jeu([Voiture("voiture.png", circuit_debut,False)])
