import pygame
from pygame.locals import QUIT,K_LEFT,K_DOWN,K_UP,K_RIGHT
import math
import neat
import sys
import time

# Importation circuit et voiture
circuit_taille=(1000, 500)
voiture_taille=(15,30)

voiture_image = pygame.image.load("voiture.png")
voiture_image = pygame.transform.scale(voiture_image, (voiture_taille[0], voiture_taille[1]))

generation = 0
class Voiture :
    def __init__(self):
        self.pos=[830,380]
        self.angle=-90
        taille=voiture_taille[0]/2
        self.coins=[
        [self.pos[0] + math.cos(math.radians(self.angle + 30)) * taille, self.pos[1] + math.sin(math.radians((self.angle + 30))) * taille],
        [self.pos[0] + math.cos(math.radians(self.angle - 30)) * taille, self.pos[1] + math.sin(math.radians((self.angle - 30))) * taille],
        [self.pos[0] + math.cos(math.radians(self.angle + 150)) * taille, self.pos[1] + math.sin(math.radians((self.angle + 150))) * taille],
        [self.pos[0] + math.cos(math.radians(self.angle -150)) * taille, self.pos[1] + math.sin(math.radians((self.angle - 150))) * taille]]
        self.rad=[]
        self.distance=0
        self.vitesse=0
        self.angle_radars=[90,30,0,-30,-90]
        self.is_alive = True
        
        self.acceleration= 0.1
        self.freinage = 0.1
        
        self.temps=0
        self.temps_debut=time.time()

        self.derniere_vitesse=time.time()

    

    def angles_voitures(self):
        taille=voiture_taille[0]/2
        left_top = [self.pos[0] + math.cos(math.radians(self.angle + 30)) * taille, self.pos[1] + math.sin(math.radians((self.angle + 30))) * taille]
        right_top = [self.pos[0] + math.cos(math.radians(self.angle - 30)) * taille, self.pos[1] + math.sin(math.radians((self.angle - 30))) * taille]
        left_bottom = [self.pos[0] + math.cos(math.radians(self.angle + 150)) * taille, self.pos[1] + math.sin(math.radians((self.angle + 150))) * taille]
        right_bottom = [self.pos[0] + math.cos(math.radians(self.angle -150)) * taille, self.pos[1] + math.sin(math.radians((self.angle - 150))) * taille]
        self.coins=[left_top,right_top,right_bottom,left_bottom,]

    def radars(self,circuit):
        for a_radar in self.angle_radars :
            longueur=0
            pos_rad = [self.pos[0] + math.cos(math.radians(self.angle + a_radar)) * longueur, self.pos[1] + math.sin(math.radians((self.angle + a_radar))) * longueur]
            while longueur<300 and not circuit.get_at((int(pos_rad[0]), int(pos_rad[1]))) == (0, 0, 0,255):
                longueur += 1
                pos_rad = [self.pos[0] + math.cos(math.radians(self.angle + a_radar)) * longueur, self.pos[1] + math.sin(math.radians((self.angle + a_radar))) * longueur]
            dist = int(math.sqrt(math.pow(pos_rad[0] - self.pos[0], 2) + math.pow(pos_rad[1] - self.pos[1], 2)))
            self.rad.append([dist,pos_rad])
    
    def data(self):
        donnees=[0,0,0,0,0]
        for i,r in enumerate(self.rad):
            donnees[i]=r[0]
        donnees.append(self.vitesse)
        donnees.append(self.temps)
        return donnees


    def verification_collision(self,circuit):
        #self.is_alive=True
        for coin in self.coins :
            if circuit.get_at((int(coin[0]), int(coin[1]))) == (0, 0, 0,255):
                self.is_alive=False
                break

    def verification_temps(self):
        if self.temps > 45 and self.is_alive:
            self.is_alive=False
        elif time.time()-self.derniere_vitesse >5:
            self.is_alive=False
    


    def draw_radar(self, screen):
        for coin in self.coins :
            pygame.draw.circle(screen, (0, 255, 0), coin, 5)
        for r in self.rad:
            dist , pos = r
            pygame.draw.line(screen, (255, 0, 0), self.pos, pos, 1)

    def affichage(self,ecran):
        self.draw_radar(ecran)

    def update(self,circuit_image):
        self.temps=time.time()-self.temps_debut
        if self.vitesse>0:
            self.derniere_vitesse=time.time()
        
        self.pos[0] += math.cos(math.radians(self.angle))*self.vitesse
        self.pos[1] += math.sin(math.radians(self.angle))*self.vitesse
        if self.pos[0] < 20:
            self.pos[0] = 20
        elif self.pos[0] > 980:
            self.pos[0] = 980
        if self.pos[1] < 20:
            self.pos[1] = 20
        elif self.pos[1] > 480:
            self.pos[1] = 480
        self.distance += self.vitesse
        self.angles_voitures()
        self.verification_collision(circuit_image)
        self.verification_temps()
        self.rad.clear()
        self.radars(circuit_image)
        
        
    def recompense(self):
        vivant=0
        if self.is_alive:
            vivant=25
        return self.distance/50 + vivant
    
    def is_alive_m(self):
        return self.is_alive
    
    def accelerer(self):
        self.vitesse += self.acceleration
    
    def freiner(self):
        self.vitesse = max(0,self.vitesse-self.freinage)


def jeu(genomes, config):

    nets = []
    voitures = []
    for id, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            g.fitness = 0
            voitures.append(Voiture())


    pygame.init()
    ecran = pygame.display.set_mode(circuit_taille)
    circuit_image = pygame.image.load("circuit2.png")
    circuit_image = pygame.transform.scale(circuit_image,circuit_taille)

    global generation
    generation += 1
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                #sys.exit(0)
                break

        for index, voiture in enumerate(voitures):
            output = nets[index].activate(voiture.data())
            max_output = max(output)
            if output[0] == max_output and voiture.vitesse > 0:
                voiture.angle -= 5
            elif output[1] == max_output and voiture.vitesse > 0:
                voiture.angle += 5
            elif output[2] == max_output:  # Ajout de contrôles d'accélération
                voiture.accelerer()
            elif output[3] == max_output:  # Ajout de contrôles de freinage
                voiture.freiner()

        total_voiture = 0
        for i, voiture in enumerate(voitures):
            if voiture.is_alive_m():
                total_voiture  += 1
                voiture.update(circuit_image)
                genomes[i][1].fitness += voiture.recompense()

        if total_voiture == 0:
            break
        ecran.blit(circuit_image, (0, 0))
        for voiture in voitures :
            if voiture.is_alive_m():
                voiture.affichage(ecran)
                
        pygame.display.update()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)
    p.run(jeu, 1000) # Lancement du jeu.