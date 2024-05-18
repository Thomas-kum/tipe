from matplotlib import pyplot as plt
import numpy as np

def affichage(x,y,legendes, titre = "", x_label = "", y_label = ""):
    for i in range(len(y)):
        plt.plot(x,y[i], label = legendes[i])
    plt.title(titre)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()