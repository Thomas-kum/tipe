import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def reLu(x):
    return max(0, x)
def tanh(x):
    return np.tanh(x)
def derivee_sigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))
def derivee_cout(valeurs_theoriques, valeurs_pratiques):
    return 2 * (valeurs_pratiques - valeurs_theoriques)
def sigmoid_V(M):
    return np.vectorize(sigmoid)(M)
def reLu_V(M):
    return np.vectorize(reLu)(M)
def tanh_V(M):
    return np.vectorize(tanh)(M)


def definition_reseau(informations_reseau):
    V, A, W, B = [], [], [], []
    A.append(np.array([[None] for _ in range(informations_reseau[0])]))
    V.append(np.array([[None] for _ in range(informations_reseau[0])]))
    for i in range(len(informations_reseau) - 1):
        A.append(np.array([[None] for _ in range(informations_reseau[i + 1])]))
        V.append(np.array([[None] for _ in range(informations_reseau[i + 1])]))
        W.append(np.array([[np.random.random_sample() for _ in range(informations_reseau[i])] for _ in range(informations_reseau[i + 1])]))
        B.append(np.array([[np.random.random_sample()] for _ in range(informations_reseau[i + 1])]))

    return V, A, W, B

def propagation(informations_reseau, V, A, W, B):
    for i in range(len(informations_reseau)-1):
        A[i + 1] = np.dot(W[i], V[i]) + B[i]
        V[i + 1] = sigmoid_V(A[i+1])
    return A, V

def retropropagation(valeurs_theoriques, A, V, W, B):

    dV = [None] * len(V)
    dW = [None] * len(W)
    dB = [None] * len(B)

    dV[-1] = derivee_cout(V[-1], valeurs_theoriques) * derivee_sigmoid(A[-1])
    dW[-1] = np.dot(dV[-1], V[-2].T)
    dB[-1] = dV[-1]

    for k in range(2, len(V)):
        dV[-k] = np.dot(W[-k + 1].T, dV[-k + 1]) * derivee_sigmoid(V[-k])
        dW[-k] = np.dot(dV[-k], V[-k - 1].T)
        dB[-k] = dV[-k]

    return dW, dB


def maj(informations_reseau, taux, W, B, dW, dB):
    for i in range(len(informations_reseau) - 1):
        W[i] = W[i] - taux * dW[i]
        B[i] = B[i] - taux * dB[i]
    return W, B


def tour(informations_reseau, taux, A, V, W, B, valeurs):
    V[0] = valeurs[0]
    A[0] = valeurs[0]

    valeurs_theoriques = valeurs[1]

    A,V = propagation(informations_reseau, V, A, W, B)

    dW, dB = retropropagation(valeurs_theoriques, A, V, W, B)

    W, B = maj(informations_reseau, taux, W, B, dW, dB)

    return W, B

def entrainement(informations_reseau, taux_apprentissage, donnees_entree):
    valeurs_entree, valeurs_theoriques = donnees_entree

    jeu_taille = len(donnees_entree)



    V, A, W, B = definition_reseau(valeurs_entree)

    for k in range(jeu_taille):
        W, B = tour(informations_reseau, taux_apprentissage, A, V, W, B, donnees_entree[k])

    print("L'entrainement est terminé !")

    return A,V,W,B

def resultat(M):
    return np.argmax(M)

def test(informations_reseau, donnees, V, A, W, B):

    images, valeurs = donnees
    succes, taille_jeu = 0, len(images)

    for k in range(taille_jeu):
        V[0] = images[k][0]
        A[0] = images[k][0]

        A,V = propagation(informations_reseau, V, A, W, B)

        valeur_pratique = resultat(V[-1])
        valeur_theorique = valeurs[k]

        if valeur_theorique == valeur_pratique:
            succes += 1

    print("Le test est terminé !")

    return round(succes/taille_jeu, 4)

def reseau(informations_reseau, donnees_entrainement, donnees_test):
    # Taille colonne 1, colonne 2, ...

    taux_apprentissage = np.random.random_sample(4)

    print("")
    print("Entrainement")
    print("")

    A,V,W,B = entrainement(informations_reseau, taux_apprentissage, donnees_entrainement)

    print("")
    print("Test")
    print("")
    
    resultat = reseau(informations_reseau, donnees_test, V, A, W, B)

    return resultat
