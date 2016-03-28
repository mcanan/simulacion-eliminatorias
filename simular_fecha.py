from simulacion import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import collections

# Inicializo matrices
probabilidades = np.loadtxt('probabilidades.txt')
probabilidades = np.reshape(probabilidades.T, (10,10,3), order='F')
probabilidades = np.swapaxes(probabilidades, 0, 1)

partidosFecha = np.array([
    [paises["Colombia"],paises["Ecuador"]],
    [paises["Uruguay"],paises["Peru"]],
    [paises["Argentina"],paises["Bolivia"]],
    [paises["Venezuela"],paises["Chile"]],
    [paises["Paraguay"],paises["Brasil"]]
    ]);

# Imprimo probabilidades
np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)

paisesOrdenados = paises.keys()
paisesOrdenados.sort()

#paisesOrdenados = collections.OrderedDict(sorted(paises.items()))
for partido in partidosFecha:
    for resultado in resultados:
        print paisesOrdenados[partido[0]], paisesOrdenados[partido[1]], resultado
        puntajes = getPuntajesIniciales()
        puntajes[partido[0],partido[1]] = resultado
        
        # Corro simulacion
        histograma = simulacion(puntajes, probabilidades, 20000)

        # Suma las probabilidades de estar en los primeros 5 puestos
        probabilidades_5_primeros = np.sum(histograma[:5,:], axis=0)
        probabilidades_4_primeros = np.sum(histograma[:4,:], axis=0)

        print '       ',
        for p in collections.OrderedDict(sorted(paises.items())):
            print  '%s  ' % p[:3].upper(),
        
        print ''
        print " <=5", probabilidades_5_primeros
        print " <=4", probabilidades_4_primeros
