import matplotlib.pyplot as plt
import numpy as np


def lineaire(mode, matrice):
    if mode == "derivee":
        return np.zeros(matrice.shape) + 1
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
    e = np.exp(matrice - np.max(matrice))
    return e / sum(e)


def ys_to_matrice(y, nb_classe):
    return np.array([[1 if i == j else 0 for i in range(nb_classe)] for j in y])


def comptage_resultats(y_pratiques, y_theoriques):
    compteur = 0
    for i in range(y_pratiques.size):
        if y_pratiques[i] == y_theoriques[i]:
            compteur += 1
    return compteur


def cout(x, y):
    return 0.5 * np.sum((x-y)**2)


def image(image):
    plt.imshow(image, cmap='gray')
    plt.show()


def image_resultat(image, valeurs, legendes):
    maxi = np.argmax(valeurs)
    couleurs = ["red" if i == maxi else "blue" for i in range(len(valeurs))]

    plt.figure()
    plt.subplot(211)
    plt.imshow(image)

    plt.subplot(212)
    plt.bar(legendes, valeurs, color=couleurs)

    plt.show()


def images_comparaison(image_originale, image_retouchee):
    plt.figure()
    plt.subplot(211)
    plt.imshow(image_originale)

    plt.subplot(212)
    plt.imshow(image_retouchee)

    plt.show()


def affichage(x, y, legendes, titre="", x_label="", y_label=""):
    for i in range(len(y)):
        plt.plot(x, y[i], label=legendes[i])
    plt.title(titre)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()
