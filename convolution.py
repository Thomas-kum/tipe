import numpy as np
from annexe import lineaire, sigmoid, ReLu, tanh, softmax

A = np.random.rand(3,4)

def retournement(matrice):
    return np.flip(matrice)


def complement(position, matrice, taille):
    n,p = matrice.shape

    matrice_2 = np.zeros((taille, taille))

    if position == "hg":
        matrice_2[:n,:p] = matrice
    elif position == "hd":
        matrice_2[:n,taille-p:] = matrice
    elif position == "bg":
        matrice_2[taille-n:,:p] = matrice
    elif position == "bd":
        matrice_2[taille-n:,taille-p:] = matrice
    return matrice_2

def convolution_2d(matrice, taille = 3, fonction_activation = lineaire):
    n,p = matrice.shape
    h = taille // 2

    W = retournement(np.random.randn(taille, taille))

    matrice_3 = np.zeros((n+ 2 * h,p + 2* h))

    matrice_3[h:-h,h:-h] = matrice


    matrice_2 = np.zeros((n,p))

    for i in range(n):
        for j in range(p):
            if i < h:
                if j < h:
                    coucou = complement("bd", matrice[:i+h, :j+h], taille)
                elif j >= p - h:
                    coucou = complement("bg", matrice[:i+h, j-h:], taille)
                else:
                    coucou = complement("hg", matrice[:i+h, j-(taille//2):j+(taille-taille//2)], taille)
            elif i >= n - h:
                if j < h:
                    coucou = complement("hd", matrice[i-h:, :j+h], taille)
                elif j >= p - taille//2:
                    coucou = complement("hg", matrice[i-h:, j-h:], taille)
                else:
                    coucou = complement("hg", matrice[i-h:, j-(taille//2):j+(taille-taille//2)], taille)
            else:
                if j < taille//2:
                    coucou = complement("bd", matrice[i-(taille//2):i+(taille-taille//2), :j+h], taille)
                elif j >= p - taille//2:

                    coucou = complement("bg", matrice[i-(taille//2):i+(taille-taille//2), j-h:], taille)
                else:
                    coucou = matrice[i-(taille//2):i+(taille-taille//2), j-(taille//2):j+(taille-taille//2)]

            matrice_2[i,j] = fonction_activation("", np.sum(coucou * W))
    return matrice_2


def convolution_2d_2(matrice, taille=3, fonction_activation=lineaire):
    n, p = matrice.shape
    h = taille // 2

    W = retournement(np.random.randn(taille, taille))

    matrice_3 = np.zeros((n + 2 * h, p + 2 * h))

    matrice_3[h:-h, h:-h] = matrice

    matrice_2 = np.zeros((n, p))

    print(W)

    for i in range(n):
        for j in range(p):
            coucou = matrice_3[i-h+1:i+taille-h+1, j-h+1:j+taille-h+1]
            matrice_2[i, j] = fonction_activation("", np.sum(coucou * W))
    return matrice_2


def convolution_3d(matrice, taille=3, fonction_activation=lineaire, k=1):
    n, p = matrice.shape
    h = taille // 2

    W = np.array([[np.random.randn(k) for _ in range(taille)] for _ in range(taille)])

    assert W.shape == (taille, taille, k)

    matrice_2 = np.zeros((n, p))

    for i in range(n):
        for j in range(p):
            if i < h:
                if j < h:
                    coucou = complement("bd", matrice[:i + h, :j + h], taille)
                elif j >= p - h:
                    coucou = complement("bg", matrice[:i + h, j - h:], taille)
                else:
                    coucou = complement("hg", matrice[:i + h, j - (taille // 2):j + (taille - taille // 2)], taille)
            elif i >= n - h:
                if j < h:
                    coucou = complement("hd", matrice[i - h:, :j + h], taille)
                elif j >= p - taille // 2:
                    coucou = complement("hg", matrice[i - h:, j - h:], taille)
                else:
                    coucou = complement("hg", matrice[i - h:, j - (taille // 2):j + (taille - taille // 2)], taille)
            else:
                if j < taille // 2:
                    coucou = complement("bd", matrice[i - (taille // 2):i + (taille - taille // 2), :j + h], taille)
                elif j >= p - taille // 2:

                    coucou = complement("bg", matrice[i - (taille // 2):i + (taille - taille // 2), j - h:], taille)
                else:
                    coucou = matrice[i - (taille // 2):i + (taille - taille // 2),
                             j - (taille // 2):j + (taille - taille // 2)]

            matrice_2[i, j] = fonction_activation("", np.sum(coucou * W))
    return matrice_2

#print(convolution_2d(A,3,lineaire))
#print(convolution_2d_2(A,3,lineaire))
print((convolution_2d(A,3,lineaire).all() == convolution_2d_2(A,3,lineaire).all()))
