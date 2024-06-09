import numpy as np
import pandas as pd
from PIL import Image


valeurs = pd.read_csv('data.csv', index_col=0)
valeurs = valeurs.to_numpy().reshape(1200)
images = np.zeros((1200, 32, 32))

for i in range(1200):
    if i < 10:
        k = '000'+str(i)
    elif i < 100:
        k = '00'+str(i)
    elif i < 1000:
        k = '0'+str(i)
    else:
        k = str(i)
    images[i] = np.array(Image.open('numbers/' + k + '.png'))
