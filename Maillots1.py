from ReseauVectorise import Reseau
from MaillotsData import images, valeurs
from annexe import ReLu, softmax, affichage
from convolution import convolution_classiques

images = images.astype("float32") / 255

liste = ["moyenne", "gaussien", "pique", "bords", "relief"]
y, legendes = [], []

for k in range(len(liste)):
    for i in range(len(images)):
        images[i] = convolution_classiques(images[i], liste[k])

    x_train, y_train = images[:1000], valeurs[:1000]
    x_test, y_test = images[1000:], valeurs[1000:]

    reseau = Reseau([32*32, 45, 45], 0.01, [ReLu, softmax])

    reseau.entrainement((x_train, y_train), 2000)

    taux_succes = reseau.taux_reussite

    legendes.append("Taux pour "+liste[k])
    y.append(taux_succes)

affichage([0.05*i*2000 for i in range(len(y[0]))], y, legendes, "Évolution du rendement", "Nombre d'entraînements", "Taux de succès")
