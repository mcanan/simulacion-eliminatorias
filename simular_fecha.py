from simulacion import *
import numpy as np

# Inicializo matrices
probabilidades = getProbabilidades('probabilidades.txt')

partidosFecha = np.array([
    [PAISES["Brasil"],PAISES["Ecuador"]],
    [PAISES["Uruguay"],PAISES["Argentina"]],
    [PAISES["Venezuela"],PAISES["Colombia"]],
    [PAISES["Chile"],PAISES["Paraguay"]],
    [PAISES["Peru"],PAISES["Bolivia"]]
    ]);

# Imprimo probabilidades
np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)

def imprimo_histograma(p5, p4):
        print '       ',
        for p in PAISES:
            print  '%s  ' % p[:3].upper(),
        
        print ''
        print " <=5", p5
        print " <=4", p4

iteraciones = 30000
ultima_fecha_jugada = 14

puntajes = getPuntajesIniciales(ultima_fecha_jugada)
histograma = getHistogramaPosiciones(puntajes, probabilidades, iteraciones)
p5_actual = np.round(np.sum(histograma[:5,:], axis=0), decimals=2)
p4_actual = np.round(np.sum(histograma[:4,:], axis=0), decimals=2)

print 'Situacion actual'
imprimo_histograma(p5_actual, p4_actual)

p5_todas = np.zeros((partidosFecha.size*3, len(PAISES)), dtype=np.float)
p4_todas = np.zeros((partidosFecha.size*3, len(PAISES)), dtype=np.float)
print 'Simulacion'
i=0
for partido in partidosFecha:
    for resultado in POSIBLES_RESULTADOS:
        print PAISES.items()[partido[0]][0], PAISES.items()[partido[1]][0], resultado
        puntajes = getPuntajesIniciales(ultima_fecha_jugada)
        puntajes[partido[0],partido[1]] = resultado
        
        # Corro simulacion
        histograma = getHistogramaPosiciones(puntajes, probabilidades, iteraciones)
        p5 = np.round(np.sum(histograma[:5,:], axis=0), decimals=2)
        p4 = np.round(np.sum(histograma[:4,:], axis=0), decimals=2)
        p5_todas[i,:]=p5-p5_actual
        p4_todas[i,:]=p4-p4_actual
        i=i+1
        imprimo_histograma(p5-p5_actual, p4-p4_actual)

print 'Uruguay posibilidades 4'
i=0
for partido in partidosFecha:
    for resultado in POSIBLES_RESULTADOS:
        print PAISES.items()[partido[0]][0], PAISES.items()[partido[1]][0], resultado, p4_todas[i,8]
        i=i+1

print 'Uruguay posibilidades 5'
i=0
for partido in partidosFecha:
    for resultado in POSIBLES_RESULTADOS:
        print PAISES.items()[partido[0]][0], PAISES.items()[partido[1]][0], resultado, p5_todas[i,8]
        i=i+1
