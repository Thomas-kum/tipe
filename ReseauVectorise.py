import numpy as np
from annexe import *


class Reseau:
    def __init__(self, dimensions, taux_apprentissage, fonctions_activation_noms):
        print("\nDEFINITION DU RESEAU VECOTIRISE")
        self.informations_reseau = dimensions
        self.taux_apprentissage = taux_apprentissage
        self.fonctions_activation = fonctions_activation_noms
        self.A, self.V = [], []
        self.W, self.B = self.definition_reseau()
        self.nb_classes = self.informations_reseau[-1]
        self.nb_entrainements, self.nb_tests = 0, 0
        self.taux_reussite = []

    def definition_reseau(self):
        w, b = [], []
        for i in range(len(self.informations_reseau) - 1):
            w.append(np.random.randn(self.informations_reseau[i + 1], self.informations_reseau[i]) / 4)
            b.append(np.random.randn(self.informations_reseau[i + 1], 1) / 4)
        return w, b

    def propagation(self, x):
        self.A = [x]
        self.V = [x]
        for i in range(len(self.informations_reseau) - 1):
            self.A.append(np.dot(self.W[i], self.V[i]) + self.B[i])
            self.V.append(self.fonctions_activation[i]("", self.A[i + 1]))

    def retropropagation(self, y, d):
        for k in range(1, len(self.V)):
            if k == 1:
                d_v = self.V[-1] - y.T
            else:
                d_v = np.dot(self.W[-k + 1].T, d_v) * self.fonctions_activation[-k]("derivee", self.V[-k])
            d_w = 1 / d * np.dot(d_v, self.V[-k - 1].T)
            d_b = 1 / d * np.sum(d_v, axis=1).reshape(self.B[-k].shape[0], 1)
            self.W[-k] -= self.taux_apprentissage * d_w
            self.B[-k] -= self.taux_apprentissage * d_b

    def entrainement(self, donnees, nb_repetitions):
        x_train, y_train = donnees
        y_train2 = ys_matriciels(y_train, self.nb_classes)
        x_train = x_train.reshape(x_train.shape[0], x_train.shape[1] * x_train.shape[2]).T
        self.nb_entrainements += x_train.shape[0]*nb_repetitions
        print("\nENTRAINEMENT")
        for i in range(nb_repetitions):
            avance = i / nb_repetitions * 100
            self.propagation(x_train)
            self.retropropagation(y_train2, x_train.shape[1])
            if avance % 5 == 0:
                resultats_corrects = comptage_resultats(np.argmax(self.V[-1], 0), y_train) / y_train.shape[0]
                self.taux_reussite.append(resultats_corrects)
                print(int(avance), " % : rendement ", int(resultats_corrects * 100))

    def test(self, donnees):
        print("\nTEST")
        x_test, y_test = donnees
        x_test = x_test.reshape(x_test.shape[0], x_test.shape[1] * x_test.shape[2])
        nombre_succes, nombre_donnees_test = 0, len(x_test)
        for i in range(nombre_donnees_test):
            avancee = i / nombre_donnees_test * 100
            self.propagation(x_test[i].reshape(x_test[i].shape[0], 1))
            valeur_pratique = np.argmax(self.V[-1])
            if avancee % 10 == 0:
                print(avancee, " % : ")
            if valeur_pratique == y_test[i]:
                nombre_succes += 1
        print("\nNombre de succès : ", nombre_succes)
        print("Taux de réussite : ", self.taux_reussite * 100, "%")
