from simulacion import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Inicializo matrices
probabilidades = getProbabilidades('utils/probabilidades_test.txt')
puntajes = getPuntajesIniciales(6)

np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)

# Corro simulacion
hz0, hz1, hz2 = getHistogramaPuntos(puntajes, probabilidades, 100)
RANGO_PUNTOS = np.arange(5,45)
f=open('asd.dat','a')
for pais in PAISES.items():
    i = pais[1]
    htotal=hz0[i]+hz1[i]+hz2[i]
    z1 = np.divide(hz0[i], np.sum(htotal), dtype=float)
    z2 = np.divide(hz1[i], np.sum(htotal), dtype=float)
    z3 = np.divide(hz2[i], np.sum(htotal), dtype=float)
    p = np.divide(htotal, np.sum(htotal), dtype=float)
    # print z1[RANGO_PUNTOS]
    print z1.size
    

    np.savetxt(f,z1.T,delimiter=",")
f.close()

a = np.asarray([ [1,2,3], [4,5,6], [7,8,9] ])
np.savetxt("foo.csv", a, delimiter=",")

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
