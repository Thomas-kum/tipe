import matplotlib.pyplot as plt  # Module pour tracer les graphiques
import numpy as np
import ast
from informations_donnees import *

def lecture_fichier(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.readlines()
            data = ast.literal_eval(data[0])
        return data
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{file_path}' n'a pas été trouvé.")
        return None
    except Exception as e:
        print(f"Erreur: Un problème est survenu lors de la lecture du fichier - {e}")
        return None

#donnees=donnees_res
donnees1 = lecture_fichier('resultats_tan_3.txt')
donnees2 = lecture_fichier('resultats_sig_2.txt')
donnees3 = lecture_fichier('resultats_re_1.txt')


def extraction(liste):
    temps,distances=[],[]
    for generation in liste:
        temps.append(generation[0][0])
        distances.append(generation[0][1])
    return temps,distances

valeurs  = extraction(donnees1)[1]
valeurs2 = extraction(donnees2)[1]
valeurs3 = extraction(donnees3)[1]

x=[k+1 for k in range(len(valeurs))]
x = np.array(x)
y1 = np.array(valeurs)
y2 = np.array(valeurs2)
y3 = np.array(valeurs3)



plt.plot(x,y1,label='Tanh')
plt.plot(x,y2,label='Sigmoid')
plt.plot(x,y3,label='ReLu')

plt.legend()
plt.title("Graphique de comparaison des fonctions d'activation")
plt.xlabel('Génération')
plt.ylabel('Distance')
plt.savefig("Comparaison")
plt.show()