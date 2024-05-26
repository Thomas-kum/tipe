import numpy as np
from annexe import ys_to_matrice, cout, comptage_resultats, softmax, ReLu
from scipy.signal import convolve2d


class ReseauConvolutif:
    def __init__(self, nb_classes, taille_image, nb_convolutions, taux_apprentissage):
        print("\nDEFINITION DU RESEAU")

        self.nb_classes = nb_classes
        self.informations_reseau = [(taille_image-2*nb_convolutions)**2, nb_classes, nb_classes]
        self.taux_apprentissage = taux_apprentissage
        self.fonctions_activation = [ReLu, softmax]
        self.nb_couches_convolutions = nb_convolutions

        self.A, self.V = [], []
        self.W, self.B, self.filtres = self.definition_reseau()

        self.nb_entrainements, self.nb_tests = 0, 0
        self.taux_reussite = []

    def definition_reseau(self):
        w, b, f = [], [], []
        for i in range(len(self.informations_reseau) - 1):
            w.append(np.random.randn(self.informations_reseau[i + 1], self.informations_reseau[i]) / 4)
            b.append(np.random.randn(self.informations_reseau[i + 1], 1) / 4)
        for k in range(self.nb_couches_convolutions):
            f.append(np.random.randint(-1, 2, (3, 3)))
        return w, b, f

    def propagation(self, x):
        self.A = [x]
        self.V = [x]
        for k in range(self.nb_couches_convolutions):
            matrice = convolve2d(self.V[-1], self.filtres[k], mode='valid')
            self.A.append(matrice)
            self.V.append(matrice)

        self.V[-1] = self.V[-1].reshape(self.V[-1].shape[0] * self.V[-1].shape[1], 1)

        for i in range(len(self.informations_reseau) - 1):
            j = i + self.nb_couches_convolutions
            self.A.append(np.dot(self.W[i], self.V[j]) + self.B[i])
            self.V.append(self.fonctions_activation[i]("", self.A[j + 1]))

    def retropropagation(self, y, d):
        y = ys_to_matrice(y, self.nb_classes).T

        for k in range(1, len(self.V)):
            if k < len(self.informations_reseau):
                if k == 1:
                    d_v = self.V[-1] - y
                else:
                    d_v = np.dot(self.W[-k + 1].T, d_v) * self.fonctions_activation[-k]("derivee", self.V[-k])

                d_w = 1 / d * np.dot(d_v, self.V[-k - 1].T)
                d_b = 1 / d * np.sum(d_v, axis=1).reshape(self.B[-k].shape[0], 1)

                self.W[-k] -= self.taux_apprentissage * d_w
                self.B[-k] -= self.taux_apprentissage * d_b
            else:
                i = k - len(self.informations_reseau)
                if i == 0:
                    d_v = np.dot(self.W[-k + 1].T, d_v)
                    self.V[-k] = self.V[-k].reshape(int(self.V[-k].shape[0] ** .5), int(self.V[-k].shape[0] ** .5))
                    d_v = d_v.reshape(self.V[-k].shape[0], self.V[-k].shape[1])

                d_f = convolve2d(self.V[-k - 1], d_v, mode='valid')
                d_v = convolve2d(self.filtres[-i], d_v, mode='full')

    def entrainement(self, donnees, nb_repetitions):
        x_train, y_train = donnees
        self.nb_entrainements += x_train.shape[0]*nb_repetitions

        print("\nENTRAINEMENT")

        for i in range(nb_repetitions):
            avance = i / nb_repetitions * 100

            for j in range(len(x_train)):
                x = x_train[j]
                y = np.array([y_train[j]])
                self.propagation(x)
                self.retropropagation(y, 60000)

            resultats_corrects = comptage_resultats(np.argmax(self.V[-1], 0), y_train)
            self.taux_reussite.append(resultats_corrects / x_train.shape[1])
            print(int(avance), " % : rendement ", resultats_corrects / x_train.shape[1])

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

        self.taux_reussite = nombre_succes / nombre_donnees_test

        print("\nNombre de succès : ", nombre_succes)
        print("Taux de réussite : ", self.taux_reussite * 100, "%")
