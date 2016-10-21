from simulacion import *
import numpy as np
import pandas as pd
import csv

# Inicializo matrices
probabilidades = getProbabilidades('probabilidades.txt')
df = pd.DataFrame()

# Corro simulacion
for fecha in np.arange(0,11):
    puntajes = getPuntajesIniciales(fecha)
    hz0, hz1, hz2 = getHistogramaPuntos(puntajes, probabilidades, 20000)
    for pais in PAISES.items():
        i = pais[1]
        htotal=hz0[i]+hz1[i]+hz2[i]
        z1 = np.divide(hz0[i], np.sum(htotal), dtype=float)
        z2 = np.divide(hz1[i], np.sum(htotal), dtype=float)
        z3 = np.divide(hz2[i], np.sum(htotal), dtype=float)
        p = np.divide(htotal, np.sum(htotal), dtype=float)
        for i in np.arange(0,99):
            if (z1[i]+z2[i]+z3[i]>0):
                print "%s,%s,%s,%s,%s,%s" % (fecha,pais[1],i,z1[i],z2[i],z3[i])

#puntos = hz0[1][np.nonzero(htotal)]
#z1 = np.divide(hz0[0][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)
#z2 = np.divide(hz1[0][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)
#z3 = np.divide(hz2[0][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)

# Imprimo probabilidades

# Grafico
#f, (ax0,ax1) = plt.subplots(2, 1, figsize=(10,4), sharex=False, sharey=False)
#sns.barplot(hz0[1][np.nonzero(htotal)], z1 + z2 + z3, color="#2ecc71", ax=ax0, label='Entre los primeros 4')
#sns.barplot(hz0[1][np.nonzero(htotal)], z2 + z3, color="#f39c12", ax=ax0, label='Queda 5')
#sns.barplot(hz0[1][np.nonzero(htotal)], z3, color="#e74c3c", ax=ax0, label='No entra en los 5')
#sns.barplot(hz0[1][np.nonzero(htotal)], p, palette="Blues_d", ax=ax1, label='Probabilidades por puntaje')
#ax0.legend(ncol=1, frameon=True)
#ax1.legend(ncol=1, frameon=True)
#plt.setp(f.axes)
#plt.tight_layout(h_pad=2)
#plt.show()
