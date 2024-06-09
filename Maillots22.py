from ReseauConvolution import ReseauConvolutif
from MaillotsData import images, valeurs
from annexe import ReLu, softmax, lineaire


x_train, y_train = images[:1000], valeurs[:1000]
x_test, y_test = images[1000:], valeurs[1000:]

x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

reseau = ReseauConvolutif(45, [
    ("C", ReLu),
    ("C", lineaire),
    ("D", ReLu),
    ("D", softmax),
    ("D", lineaire)
], 0.01, 1000, (x_train, y_train))

reseau.entrainement()
