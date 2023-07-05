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
donnees = lecture_fichier('resultats_sig_2.txt')

taille = 0


valeurs  = []
valeurs2 = []
valeurs3 = []
valeurs4 = []

temps=[]
distances=[]

texte=["arrivee","vitesse","temps","bord"]

print("Taille de la base de données : ",len(donnees))

donnees_finales=[]

for generation in donnees:
    if type(generation)==list:
        donnees_finales.append(generation)
        taille+=1
        cpt={"arrivee":0,"vitesse":0,"temps":0,"bord":0}

        for ele in generation[0][2].keys():
            cpt[ele]=generation[0][2][ele]
        
        valeurs.append(cpt["arrivee"])
        valeurs2.append(cpt["vitesse"])
        valeurs3.append(cpt["temps"])
        valeurs4.append(cpt["bord"])

        temps.append(generation[0][0])
        distances.append(generation[0][1])


assert len(valeurs) == taille and len(valeurs) == len(valeurs2) and len(valeurs)==len(valeurs3) and len(valeurs)==len(valeurs4)

valeurs=np.array(valeurs)
valeurs2=np.array(valeurs2)
valeurs3=np.array(valeurs3)
valeurs4=np.array(valeurs4)

mots=[str(k+1) for k in range(taille)]

weight_counts={
    "Arrivées":valeurs,
    "Vitesse":valeurs2,
    "Temps":valeurs3,
    "Bord":valeurs4
}

width = 0.7

fig, ax = plt.subplots()
bottom = np.zeros(taille)

for boolean, weight_count in weight_counts.items():
    p = ax.bar(mots, weight_count, width, label=boolean, bottom=bottom)
    bottom += weight_count

ax.set_title("Nombre de voitures arrivées")
ax.legend(loc="upper right")

plt.show()
plt.savefig("Version 1 - Données")

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(temps, color='blue', label='Temps')
ax1.set_ylabel('Valeurs')
ax2.plot(distances, color='red', label='Distance')
ax2.set_xlabel('Indices')
ax2.set_ylabel('Valeurs')
ax1.legend()
ax2.legend()


plt.show()
plt.savefig("Version 1 - Temps + distance")