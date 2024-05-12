from reseau import ReseauConvolutif
import numpy as np
import keras
from keras import layers


(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

assert x_train.shape == (60000, 28, 28)
print("Données d'entrainement : nombre de données ", x_train.shape[0], " ; taille de l'image ", x_train[0].shape[0], x_train[0].shape[1])
print("Données de test : nombre de données ", x_test.shape[0], " ; taille de l'image ", x_test[0].shape[1], x_test[0].shape[1])

y_train = keras.utils.to_categorical(y_train)
y_test = keras.utils.to_categorical(y_test)


reseau_mnist = ReseauConvolutif([28*28, 28*28, 10],np.random.rand(),"sigmoid",(x_train, y_train), (x_test, y_test))
reseau_mnist.entrainement()
reseau_mnist.test()