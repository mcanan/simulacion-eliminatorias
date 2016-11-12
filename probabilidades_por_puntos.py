from simulacion import *
import numpy as np
import pandas as pd
import csv

# Inicializo matrices
probabilidades = getProbabilidades('probabilidades.txt')
df = pd.DataFrame()

# Corro simulacion
for fecha in np.arange(11,12):
    puntajes = getPuntajesIniciales(fecha)
    hz0, hz1, hz2 = getHistogramaPuntos(puntajes, probabilidades, 30000)
    for pais in PAISES.items():
        i = pais[1]
        htotal=hz0[i]+hz1[i]+hz2[i]
        z1 = np.round(np.divide(hz0[i], np.sum(htotal), dtype=float),3)
        z2 = np.round(np.divide(hz1[i], np.sum(htotal), dtype=float),3)
        z3 = np.round(np.divide(hz2[i], np.sum(htotal), dtype=float),3)
        p = np.round(np.divide(htotal, np.sum(htotal), dtype=float),3)
        paisNombre = pais[0]
        partido = getPartido(fecha,pais[1])
        for i in np.arange(0,99):
            if (z1[i]+z2[i]+z3[i]>0):
                print "%s,%s,%s,%s,%s,%s,%s,%s" % (fecha,pais[1],i,z1[i],z2[i],z3[i],partido,paisNombre)
                partido = ""
                paisNombre = ""
