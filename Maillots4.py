import numpy as np
from matplotlib import pyplot as plt
from MaillotsData import images, valeurs
from annexe import affichage


x_train, y_train = images[:1000], valeurs[:1000]
x_test, y_test = images[1000:], valeurs[1000:]
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255


def distance(p1, p2):
    d = 0
    for i in range(p1.shape[0]):
        for j in range(p1.shape[1]):
            d += (p1[i, j] - p2[i, j])**2
    return d**0.5


def voisins(x, k):
    indices = sorted(range(len(x_train)), key=lambda i: distance(x, x_train[i]))
    return indices[:k]


def plus_frequent(liste):
    compte = {}
    for e in liste:
        compte[e] = compte.get(e, 0) + 1
    return max(compte, key=compte.get)


def knn(x, k):
    V = voisins(x, k)
    return plus_frequent([y_train[i] for i in V])


def precision(k):
    n = 0
    for i in range(len(x_test)):
        if knn(x_test[i], k) == y_test[i]:
            n += 1
    return n / len(x_test)


ks = range(1, 10)
resultats = [precision(k) for k in ks]
affichage(ks, [resultats], ["Précision en fonction de k"], "k voisins", "Rendement de l'algorithme")
