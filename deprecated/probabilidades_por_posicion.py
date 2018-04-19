from simulacion import *
from math import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Inicializo matrices
probabilidades = getProbabilidades('probabilidades.txt')
puntajesIniciales = getPuntajesIniciales(6)

# Corro simulacion
histograma = getHistogramaPosiciones(puntajesIniciales, probabilidades, 200)

# Imprimo histograma
np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)
print '      ',
for p in PAISES:
    print  '%s  ' % p[:3].upper(),
print ''
for i in range(1,11):
    print "%2d " % i, histograma[i-1,:]

# Calculo orden
orden = []
for i in range(0,10):
    acumulado_posicion = np.sum(histograma[:(i+1),:], axis=0)
    acumulado_posicion[orden] = 0
    x = np.argmax(acumulado_posicion)
    orden.append(x)

# Grafico
f, ax = plt.subplots(2, 5, figsize=(15,5), sharex=False, sharey=True)
x = np.arange(1, 11)
for i,v in enumerate(orden):
    axs = ax[i>4,i%5]
    sns.barplot(x, histograma[:,v], palette="BuGn_d", ax=axs)
    axs.set_title(PAISES.items()[v][0])

plt.setp(f.axes, yticks=np.arange(0,1.01,.1), xticks=np.arange(0,11))
plt.tight_layout(h_pad=2)
plt.show()
