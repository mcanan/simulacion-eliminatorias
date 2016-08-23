from simulacion import *
import numpy as np

# Inicializo matrices
probabilidades = getProbabilidades('probabilidades.txt')

partidosFecha = np.array([
    [PAISES["Colombia"],PAISES["Ecuador"]],
    [PAISES["Uruguay"],PAISES["Peru"]],
    [PAISES["Argentina"],PAISES["Bolivia"]],
    [PAISES["Venezuela"],PAISES["Chile"]],
    [PAISES["Paraguay"],PAISES["Brasil"]]
    ]);

# Imprimo probabilidades
np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)

for partido in partidosFecha:
    for resultado in POSIBLES_RESULTADOS:
        print PAISES.items()[partido[0]][0], PAISES.items()[partido[1]][0], resultado
        puntajes = getPuntajesIniciales(6)
        puntajes[partido[0],partido[1]] = resultado
        
        # Corro simulacion
        histograma = getHistogramaPosiciones(puntajes, probabilidades, 100)

        # Suma las probabilidades de estar en los primeros 5 puestos
        probabilidades_5_primeros = np.sum(histograma[:5,:], axis=0)
        probabilidades_4_primeros = np.sum(histograma[:4,:], axis=0)

        print '       ',
        for p in PAISES:
            print  '%s  ' % p[:3].upper(),
        
        print ''
        print " <=5", probabilidades_5_primeros
        print " <=4", probabilidades_4_primeros
