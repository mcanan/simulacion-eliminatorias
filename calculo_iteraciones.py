from simulacion import *
from math import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Inicializo matrices
probabilidades = getProbabilidades('probabilidades.txt')
puntajesIniciales = getPuntajesIniciales(6)

# Corro simulaciones
cantidad_iteraciones = 20;

todos_histogramas = np.zeros((cantidad_iteraciones,10,10))
for i in range(0,cantidad_iteraciones):
    print i
    histograma = getHistogramaPosiciones(puntajesIniciales, probabilidades, 20000)
    todos_histogramas[i]=histograma

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

print np.absolute(np.amax(todos_histogramas,axis=0)-np.amin(todos_histogramas,axis=0))
print np.std(todos_histogramas,axis=0)
print np.average(todos_histogramas,axis=0)
