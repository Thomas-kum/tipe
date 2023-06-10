import math

def transformation(coordonnees,distance,angle):
    x=coordonnees[0]+distance*math.cos(angle)
    y=coordonnees[1]+distance*math.sin(angle)
    x=round(x)
    y=round(y)
    return x,y
