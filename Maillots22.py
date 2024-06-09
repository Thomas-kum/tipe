import numpy as np
from scipy.signal import convolve2d
from annexe import ReLu, softmax, ys_matriciels, tanh, affichage

n = 1000

from MaillotsData import images, valeurs

x_train, y_train = images[:n], valeurs[:n]
x_test, y_test = images[n:], valeurs[n:]

x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

# Définitions générales
nb_train = len(x_train)
nb_entrainement = 1000
taux = 0.01
F1 = np.random.randn(3, 3)
B1 = np.random.randn(30, 30)
F2 = np.random.randn(3, 3)
B2 = np.random.randn(28, 28)
W3 = np.random.randn(46, 28 * 28)
B3 = np.random.randn(46, 1)
W4 = np.random.randn(46, 46)
B4 = np.random.randn(46, 1)

print("debut")
succes = []
for j in range(nb_entrainement):
    d = {}
    compteur = 0
    statut = True
    for i in range(nb_train):
        # Propagation

        V0 = x_train[i]
        A1 = convolve2d(V0, F1, mode='valid') + B1
        V1 = ReLu("", A1)
        V2 = convolve2d(V1, F2, mode='valid') + B2
        V22 = V2.reshape(28 * 28, 1)
        A3 = np.dot(W3, V22) + B3
        V3 = ReLu("", A3)
        A4 = np.dot(W4, V3) + B4
        V4 = softmax("", A4)

        y_t = np.argmax(V4)

        if np.isnan(V2).any():
            print(j, i)
            print(dV2, F2, A1)
            # print(F1, B1, F2, B2, W3, B3)
            statut = False
            break

        if y_t == y_train[i]:
            compteur += 1
            if y_t in d:
                d[y_t] += 1
            else:
                d[y_t] = 1

        # Rétropopagation
        y = ys_matriciels([y_train[i]], 46).T

        assert y.shape == V4.shape
        dV4 = V4 - y
        dW4 = np.dot(dV4, V3.T)
        dB4 = dV4
        W4 -= taux * dW4
        B4 -= taux * dB4

        dV3 = np.dot(W4.T, dV4) * ReLu("derivee", A3)
        dW3 = np.dot(dV3, V22.T)
        dB3 = dV3
        W3 -= taux * dW3
        B3 -= taux * dB3

        dV2 = np.dot(W3.T, dV3)
        dV2 = dV2.reshape(28, 28)
        dF2 = convolve2d(V1, dV2, mode='valid')
        dB2 = dV2
        assert dB2.shape == dV2.shape
        assert F2.shape == dF2.shape
        F2 -= taux * dF2
        B2 -= taux * dB2

        dV1 = convolve2d(dV2, np.flip(F2), mode='full') * ReLu("derivee", A1)
        dF1 = convolve2d(V0, dV1, mode='valid')
        dB1 = dV1
        assert dB1.shape == dV1.shape
        assert F1.shape == dF1.shape
        F1 -= taux * dF1
        B1 -= taux * dB1

    print(j, d)
    succes.append(compteur / nb_train)
    if not statut:
        break

affichage([i for i in range(len(succes))], [succes], ["nombre de succès"], "nombre de succès par itération",
          "nombre de succès", "itération")