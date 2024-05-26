from ReseauConvolution import ReseauConvolutif
from MaillotsData import images, valeurs


x_train, y_train = images[:1000], valeurs[:1000]
x_test, y_test = images[1000:], valeurs[1000:]

x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

taille = (32-2*5)

reseau = ReseauConvolutif(45, 32, 2, 0.01)
reseau.entrainement((x_train, y_train), 10)
