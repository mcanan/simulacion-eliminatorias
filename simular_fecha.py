from simulacion import *
import numpy as np

# Inicializo matrices
probabilidades = getProbabilidades('probabilidades.txt')

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

for partido in partidosFecha:
    for resultado in resultados:
        print paises.items()[partido[0]][0], paises.items()[partido[1]][0], resultado
        puntajes = getPuntajesIniciales()
        puntajes[partido[0],partido[1]] = resultado
        
        # Corro simulacion
        histograma = simulacion(puntajes, probabilidades, 20000)

        # Suma las probabilidades de estar en los primeros 5 puestos
        probabilidades_5_primeros = np.sum(histograma[:5,:], axis=0)
        probabilidades_4_primeros = np.sum(histograma[:4,:], axis=0)

        print '       ',
        for p in paises:
            print  '%s  ' % p[:3].upper(),
        
        print ''
        print " <=5", probabilidades_5_primeros
        print " <=4", probabilidades_4_primeros
