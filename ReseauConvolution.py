import numpy as np
from annexe import ys_matriciels, comptage_resultats
from scipy.signal import convolve2d


class ReseauConvolutif:
    def __init__(self, nb_classes, dimensions, taux_apprentissage, nb_rep_entrainement, donnees_entrainement):
        print("\nDEFINITION DU RÉSEAU")

        self.nb_classes = nb_classes
        self.informations_reseau = dimensions
        self.fonctions_activation = []

        self.taille_convolution = 2
        self.taille_dense = 3

        self.taux_apprentissage = taux_apprentissage
        self.nb_rep_entrainement = nb_rep_entrainement
        self.donnees_entrainement = donnees_entrainement

        self.A, self.V = [], []
        self.W, self.B, self.filtres, self.b2 = self.definition_reseau(donnees_entrainement[0].shape[1])

        self.nb_entrainements, self.nb_tests = 0, 0
        self.taux_reussite = []
        print(self.fonctions_activation)

    def definition_reseau(self, hauteur_image):
        w, b, f, b2 = [], [], [], []
        for k in range(len(self.informations_reseau)-1):
            if self.informations_reseau[k][0] == "C":
                f.append(np.random.randn(3, 3))
                b2.append(np.random.randn())
                self.fonctions_activation.append(self.informations_reseau[k][1])
            else:
                if self.informations_reseau[k-1][0] == "C":
                    w.append(np.random.randn(self.nb_classes, (hauteur_image-2*len(f))**2))
                    b.append(np.random.randn(self.nb_classes, 1))
                    self.fonctions_activation.append(self.informations_reseau[k][1])
                elif k == len(self.informations_reseau)-1:
                    w.append(np.random.randn(self.nb_classes, self.nb_classes))
                    b.append(np.random.randn(self.nb_classes, 1))
                else:
                    w.append(np.random.randn(self.nb_classes, self.nb_classes))
                    b.append(np.random.randn(self.nb_classes, 1))
                    self.fonctions_activation.append(self.informations_reseau[k][1])

        for i in b2:
            print(i.shape)
        return w, b, f, b2

    def propagation(self, x):
        self.A = [x]
        self.V = [x]
        for k in range(len(self.filtres)):
            self.A.append(convolve2d(self.V[-1], self.filtres[k], mode='valid') + self.b2[k])
            self.V.append(self.fonctions_activation[k]("", self.A[-1]))

        self.V[-1] = self.V[-1].reshape(self.V[-1].shape[0] * self.V[-1].shape[1], 1)

        for i in range(len(self.informations_reseau) - len(self.filtres) - 1):
            self.A.append(np.dot(self.W[i], self.V[-1]) + self.B[i])
            self.V.append(self.fonctions_activation[i + len(self.filtres)]("", self.A[-1]))

    def retropropagation(self, y):
        y = y.T

        for k in range(1, self.taille_dense):
            if k == 1:
                d_v = self.V[-1] - y
            else:
                d_v = np.dot(self.W[-k + 1].T, d_v) * self.fonctions_activation[-k]("derivee", self.A[-k])
            d_w = np.dot(d_v, self.V[-k - 1].T)
            d_b = np.sum(d_v, axis=1).reshape(self.B[-k].shape[0], 1)

            self.W[-k] -= self.taux_apprentissage * d_w
            self.B[-k] -= self.taux_apprentissage * d_b

        d_v = np.dot(self.W[-self.taille_dense + 1].T, d_v)
        self.V[-k] = self.V[-k].reshape(int(self.V[-k].shape[0] ** .5), int(self.V[-k].shape[0] ** .5))
        d_v = d_v.reshape(self.V[-k].shape[0], self.V[-k].shape[1])

        for k in range(self.taille_dense, self.taille_convolution + self.taille_dense):
            i = k - self.taille_dense

            d_f = convolve2d(self.V[-k - 1], d_v, mode='valid')
            d_b2 = np.sum(d_v)
            d_v = convolve2d(d_v, np.flip(self.filtres[-i]), mode='full') * self.fonctions_activation[-k]("derivee", self.A[-k])

            self.filtres[-i] = self.filtres[-i] - self.taux_apprentissage * d_f
            self.b2[-(i + 1)] = self.b2[-(i + 1)] - self.taux_apprentissage * d_b2

    def entrainement(self):
        x_train, y_train = self.donnees_entrainement
        self.nb_entrainements += x_train.shape[0] * self.nb_rep_entrainement

        print("\nENTRAINEMENT")

        for i in range(self.nb_rep_entrainement):
            avance = i / self.nb_rep_entrainement * 100
            corr = 0

            for j in range(len(x_train)):
                x = x_train[j]
                y = np.array([y_train[j]])
                self.propagation(x)
                self.retropropagation(ys_matriciels(y, self.nb_classes))

                corr += comptage_resultats(np.argmax(self.V[-1], 0) + 1, y)

            if avance % 5 == 0:
                resultat = corr / len(x_train)
                self.taux_reussite.append(resultat)
                print(int(avance), " % : rendement ", int(resultat * 100))

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