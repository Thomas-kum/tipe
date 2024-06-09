import numpy as np
import keras
from keras import layers
from MaillotsData import images, valeurs

nb_classes = 46
taille = (32, 32, 1)
x_train, y_train = images[:1000], valeurs[:1000]
x_test, y_test = images[1000:], valeurs[1000:]
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)
print("x_train shape:", x_train.shape)
print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")

y_train = keras.utils.to_categorical(y_train, nb_classes)
y_test = keras.utils.to_categorical(y_test, nb_classes)

reseau = keras.Sequential(
    [
        keras.Input(shape=taille),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.Flatten(),
        layers.Dense(nb_classes, activation="softmax"),
    ]
)

reseau.summary()
batch_size = 128
epochs = 1000
reseau.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
reseau.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

resultats = reseau.evaluate(x_test, y_test, verbose=0)
print("Taux de succès : ", resultats[1])
