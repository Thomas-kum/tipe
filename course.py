import pygame
from pygame.locals import QUIT,K_LEFT,K_DOWN,K_UP,K_RIGHT
import math
from random import randint
import neat
import sys



# Importation circuit et voiture
circuit_taille=(1000, 500)
largueur_voiture=40
longueur_voiture = 40
voiture_image = pygame.image.load("car.png")
voiture_image = pygame.transform.scale(voiture_image, (largueur_voiture, longueur_voiture))







generation = 0
class Voiture :
    def __init__(self):
        self.pos=[500,50]
        self.angle=0
        taille=largueur_voiture/2
        self.coins=[
        [self.pos[0] + math.cos(math.radians(self.angle + 30)) * taille, self.pos[1] + math.sin(math.radians((self.angle + 30))) * taille],
        [self.pos[0] + math.cos(math.radians(self.angle - 30)) * taille, self.pos[1] + math.sin(math.radians((self.angle - 30))) * taille],
        [self.pos[0] + math.cos(math.radians(self.angle + 150)) * taille, self.pos[1] + math.sin(math.radians((self.angle + 150))) * taille],
        [self.pos[0] + math.cos(math.radians(self.angle -150)) * taille, self.pos[1] + math.sin(math.radians((self.angle - 150))) * taille]]
        self.rad=[]
        self.distance=0
        self.vitesse=10
        self.angle_radars=[90,30,0,-30,-90]
        self.is_alive = True
    

    def corners(self):
        taille=largueur_voiture/2
        left_top = [self.pos[0] + math.cos(math.radians(self.angle + 30)) * taille, self.pos[1] + math.sin(math.radians((self.angle + 30))) * taille]
        right_top = [self.pos[0] + math.cos(math.radians(self.angle - 30)) * taille, self.pos[1] + math.sin(math.radians((self.angle - 30))) * taille]
        left_bottom = [self.pos[0] + math.cos(math.radians(self.angle + 150)) * taille, self.pos[1] + math.sin(math.radians((self.angle + 150))) * taille]
        right_bottom = [self.pos[0] + math.cos(math.radians(self.angle -150)) * taille, self.pos[1] + math.sin(math.radians((self.angle - 150))) * taille]
        self.coins=[left_top,right_top,right_bottom,left_bottom,]

    def radars(self,circuit):
        
        
        
        for a_radar in self.angle_radars :
            longueur=0
            pos_rad = [self.pos[0] + math.cos(math.radians(self.angle + a_radar)) * longueur, self.pos[1] + math.sin(math.radians((self.angle + a_radar))) * longueur]
            
            while longueur<200 and not circuit.get_at((int(pos_rad[0]), int(pos_rad[1]))) == (0, 0, 0,255):
                
                longueur += 1
                pos_rad = [self.pos[0] + math.cos(math.radians(360-self.angle + a_radar)) * longueur, self.pos[1] + math.sin(math.radians((360-self.angle + a_radar))) * longueur]
            
            self.rad.append([longueur,pos_rad])

        
    
    def data(self):
        D_rad=[0,0,0,0,0]
        for i,r in enumerate(self.rad):
            D_rad[i]=r[0]
        return D_rad   


    def collision(self,circuit):
        
        self.is_alive=True
        for coin in self.coins :
            
            if circuit.get_at((int(coin[0]), int(coin[1]))) == (0, 0, 0,255):
                
                self.is_alive=False
                break
    


    def draw_radar(self, screen):
        for coin in self.coins :
            pygame.draw.circle(screen, (0, 255, 0), coin, 5)
        for r in self.rad:
            dist , pos = r
            pygame.draw.line(screen, (255, 0, 0), self.pos, pos, 1)
    def affichage(self,ecran):
        
        #rotated_voiture_image = pygame.transform.rotate(voiture_image, int(math.degrees(self.angle)))
        #voiture_rect = rotated_voiture_image.get_rect(center=(self.pos[0], self.pos[1]))
        #ecran.blit(rotated_voiture_image, voiture_rect)
        self.draw_radar(ecran)

    def update(self,circuit_image):
        
        self.pos[0] += math.cos(self.angle)*self.vitesse
        self.pos[1] += math.sin(self.angle)*self.vitesse
        if self.pos[0] < 20:
            self.pos[0] = 20
        elif self.pos[0] > 920:
            self.pos[0] = 920
        if self.pos[1] < 20:
            self.pos[1] = 20
        elif self.pos[1] > 480:
            self.pos[1] = 480
        self.distance += self.vitesse
        self.corners()
        self.collision(circuit_image)
        self.rad.clear()
        self.radars(circuit_image)
        
        
        
    
    def is_alive_m(self):
        return self.is_alive
    




#Boucle pincipale

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
    circuit_image = pygame.image.load("circuit.png")
    circuit_image = pygame.transform.scale(circuit_image,circuit_taille)    
    global generation
    generation += 1
    

    while True:
            
                for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit(0)

                
                
            
                for index, voiture in enumerate(voitures):
                    output = nets[index].activate(voiture.data())
                    i = output.index(max(output))
                    if i == 0:
                        voiture.angle += 10
                    else:
                        voiture.angle -= 10
                    
                
                total_voiture = 0
                for i, voiture in enumerate(voitures):
                    if voiture.is_alive_m():
                        total_voiture  += 1
                        
                        voiture.update(circuit_image)
                        genomes[i][1].fitness += voiture.distance/50

                if total_voiture == 0:
                    break
                ecran.blit(circuit_image, (0, 0))
        
                for voiture in voitures :
                    if voiture.is_alive_m():
                        voiture.affichage(ecran)
                
                
                pygame.display.update()

                
                pygame.time.Clock().tick(0)

            

if __name__ == "__main__":
    
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)


    
    p.run(jeu, 150)