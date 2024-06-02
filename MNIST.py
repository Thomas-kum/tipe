from ReseauVectorise import Reseau
from annexe import ReLu, sigmoid, tanh, softmax
from matplotlib import pyplot as plt
from graphes import affichage

import numpy as np
import keras
from keras import layers


(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

reseau_mnist = Reseau([28*28, 10, 10], 0.10, [ReLu, softmax])
reseau_mnist.entrainement((x_train, y_train), 500)
reseau_mnist.test((x_test, y_test))

taux_succes = reseau_mnist.taux_reussite

affichage([0.05*i*500 for i in range(len(taux_succes))], [taux_succes], ["Taux de succès"], "Taux de succès en fonction du nombre d'entraînements", "Nombre d'entraînements", "Taux de succès")
