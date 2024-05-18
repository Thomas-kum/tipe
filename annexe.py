import numpy as np


def lineaire(mode, matrice):
    if mode == "derivee":
        return np.zeros(matrice.shape)
    return matrice


def sigmoid(mode, matrice):
    if mode == "derivee":
        return sigmoid("", matrice) * (1 - sigmoid("", matrice))
    return 1 / (1 + np.exp(-matrice))


def ReLu(mode, matrice):
    if mode == "derivee":
        return matrice > 0
    return np.maximum(matrice, 0)


def tanh(mode, matrice):
    if mode == "derivee":
        return 1 - tanh("", matrice) ** 2
    return np.tanh(matrice)


def softmax(mode, matrice):
    if mode == "derivee":
        print("Erreur : la dérivée de la fonction softmax n'est pas définie")
        return None
    return np.exp(matrice) / sum(np.exp(matrice))


def ys_to_matrice(y, nb_classe):
    return np.array([[1 if i == j else 0 for i in range(nb_classe)] for j in y])


def comptage_resultats(y_pratiques, y_theoriques):
    compteur = 0
    for i in range(y_pratiques.size):
        if y_pratiques[i] == y_theoriques[i]:
            compteur += 1
    return compteur
