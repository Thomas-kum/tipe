import numpy as np
from MaillotsData import images, valeurs
from annexe import ReLu, softmax, lineaire
from matplotlib import pyplot as plt


x_train, y_train = images[:1000], valeurs[:1000]
x_test, y_test = images[1000:], valeurs[1000:]

x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

assert x_train.shape == (1000, 32, 32) and y_train.shape == (1000,)
assert x_test.shape == (200, 32, 32)
print(y_train.shape)


def distance(p1, p2):
    d = 0
    for i in range(p1.shape[0]):
        for j in range(p1.shape[1]):
            d += (p1[i, j] - p2[i, j])**2
    return d**0.5

print("nombre de données dans x_train :", len(x_train))
print("nombre de données dans x_test :", len(x_test))

def voisins(x, k):
    indices = sorted(range(len(x_train)), key=lambda i: distance(x, x_train[i]))
    return indices[:k]

def plus_frequent(L):
    compte = {}
    for e in L:
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

def plot_precision(kmax):
    import matplotlib.pyplot as plt
    R = range(1, kmax)
    L = [precision(k) for k in R]
    print(L)
    plt.plot(R, L)
    plt.show()

plot_precision(10)