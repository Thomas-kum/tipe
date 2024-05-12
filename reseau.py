import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def reLu(x):
    return max(0, x)
def tanh(x):
    return np.tanh(x)
def derivee_sigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))
def derivee_reLu(x):
    return 1 if x > 0 else 0
def derivee_tanh(x):
    return 1 - tanh(x) ** 2
def derivee_cout(valeurs_theoriques, valeurs_pratiques):
    return 2 * (valeurs_pratiques - valeurs_theoriques)
def ligne_to_colonne(M):
    return M.reshape(M.shape[0] , 1)
def matrice_to_colonne(M):
    return M.reshape(M.shape[0] * M.shape[1], 1)

class ReseauConvolutif:

    def __init__(self, info, taux, fonction_nom, data_train, data_test):
        self.informations_reseau = info
        self.taux_apprentissage = taux

        if fonction_nom == "sigmoid":
            self.fonction = np.vectorize(sigmoid)
            self.fonction_derivee = np.vectorize(derivee_sigmoid)
        elif fonction_nom == "reLu":
            self.fonction = np.vectorize(reLu)
            self.fonction_derivee = np.vectorize(derivee_reLu)
        else:
            self.fonction = np.vectorize(tanh)
            self.fonction_derivee = np.vectorize(derivee_tanh)

        self.x_train, self.y_train = data_train
        self.x_test, self.y_test = data_test

        self.A, self.V, self.W, self.B = self.definition_reseau()

        self.taille_jeu_entrainement = len(self.x_train)

        self.nombre_succes = 0
        self.taille_jeu_test = len(self.x_test)


    def definition_reseau(self):

        print("\nDEFINITION DU RESEAU")
        A, V, W, B = [], [], [], []

        A.append(np.array([[None] for _ in range(self.informations_reseau[0])]))
        V.append(np.array([[None] for _ in range(self.informations_reseau[0])]))

        for i in range(len(self.informations_reseau) - 1):
            A.append(np.array([[None] for _ in range(self.informations_reseau[i + 1])]))
            V.append(np.array([[None] for _ in range(self.informations_reseau[i + 1])]))

            W.append(np.random.uniform(-1,1,(self.informations_reseau[i + 1], self.informations_reseau[i])))
            B.append(np.random.uniform(-1,1,(self.informations_reseau[i + 1], 1)))
        return A, V, W, B

    def affichage_reinitialisation(self, total):
        self.nombre_actuel = 0
        self.nombre_total = total
        self.nombre_affiche = -1

    def affichage(self):
        calcul = int(self.nombre_actuel / self.nombre_total * 10)
        if calcul > self.nombre_affiche:
            self.nombre_affiche += 1
            print("Progression : ", self.nombre_affiche * 10, "%")
    def propagation(self, x):
        if x.shape[1] != 1:
            x = matrice_to_colonne(x)

        self.A[0] = x
        self.V[0] = x

        for i in range(len(self.informations_reseau) - 1):
            self.A[i + 1] = np.dot(self.W[i], self.V[i]) + self.B[i]
            self.V[i + 1] = self.fonction(self.A[i + 1])

    def retropropagation(self, y):
        dV = [None] * len(self.V)
        dW = [None] * len(self.W)
        dB = [None] * len(self.B)

        dV[-1] = derivee_cout(self.V[-1], y) * self.fonction(self.A[-1])
        dW[-1] = np.dot(dV[-1], self.V[-2].T)
        dB[-1] = dV[-1]

        for k in range(2, len(self.V)):
            dV[-k] = np.dot(self.W[-k + 1].T, dV[-k + 1]) * self.fonction(self.V[-k])
            dW[-k] = np.dot(dV[-k], self.V[-k - 1].T)
            dB[-k] = dV[-k]

        for i in range(len(self.informations_reseau) - 1):
            self.W[i] = self.W[i] - self.taux_apprentissage * dW[i]
            self.B[i] = self.B[i] - self.taux_apprentissage * dB[i]

    def entrainement(self):

        print("\nDEBUT DE L'ENTRAINEMENT")

        self.affichage_reinitialisation(len(self.x_train))

        for k in range(len(self.x_train)):
            self.nombre_actuel += 1
            self.affichage()
            self.propagation(self.x_train[k])
            self.retropropagation(ligne_to_colonne(self.y_train[k]))

        print("FIN DE L'ENTRAINEMENT")

    def test(self):

        print("\nDEBUT DU TEST")

        self.affichage_reinitialisation(len(self.x_test))

        for k in range(self.taille_jeu_test):
            self.propagation(self.x_test[k])

            self.nombre_actuel += 1
            self.affichage()

            valeur_pratique = np.argmax(self.V[-1])
            valeur_theorique = np.argmax(self.y_test[k])

            if valeur_theorique == valeur_pratique:
                self.nombre_succes += 1

        print("FIN DU TEST")
        print("\nNombre de succès : ", self.nombre_succes)
        print("Taux de réussite : ", self.nombre_succes / self.taille_jeu_test * 100, "%")