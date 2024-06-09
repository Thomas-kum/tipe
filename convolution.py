import numpy as np
from annexe import lineaire


def convolution_2d(matrice, taille=3, fonction_activation=lineaire):
    n, p = matrice.shape
    h = taille // 2
    W = np.flip(np.random.randn(taille, taille))
    matrice_3 = np.zeros((n + 2 * h, p + 2 * h))
    matrice_3[h:-h, h:-h] = matrice
    matrice_2 = np.zeros((n, p))
    for i in range(n):
        for j in range(p):
            coucou = matrice_3[i-h+1:i+taille-h+1, j-h+1:j+taille-h+1]
            matrice_2[i, j] = fonction_activation("", np.sum(coucou * W))
    return matrice_2

def convolution_classiques(matrice, type):
    n, p = matrice.shape
    h = 1
    filtre = np.zeros((3,3))
    if type == "moyenne":
        filtre = 1/9 * np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    elif type == "gaussien":
        filtre = 1/16 * np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    elif type == "pique":
        filtre = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    elif type == "bords":
        filtre = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    elif type == "relief":
        filtre = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
    matrice_3 = np.zeros((n + 2 * h, p + 2 * h))
    matrice_3[h:-h, h:-h] = matrice
    matrice_2 = np.zeros((n, p))
    for i in range(n):
        for j in range(p):
            coucou = matrice_3[i-h+1:i+3-h+1, j-h+1:j+3-h+1]
            matrice_2[i, j] = np.sum(coucou * np.flip(filtre))
    return matrice_2
