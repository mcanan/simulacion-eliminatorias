from simulacion import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import collections

# Inicializo matrices
probabilidades = np.loadtxt('probabilidades.txt')
probabilidades = np.reshape(probabilidades.T, (10,10,3), order='F')
probabilidades = np.swapaxes(probabilidades, 0, 1)
puntajes = getPuntajesIniciales()

# Corro simulacion
histograma = simulacion(puntajes, probabilidades, 20000)

# Suma las probabilidades de estar en los primeros 5 puestos
probabilidades_5_primeros = np.sum(histograma[:5,:], axis=0)
probabilidades_4_primeros = np.sum(histograma[:4,:], axis=0)

# Imprimo probabilidades
np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)
print '       ',
for p in collections.OrderedDict(sorted(paises.items())):
    print  '%s  ' % p[:3].upper(),
print ''
print " <=5", probabilidades_5_primeros
print "  >5", 1-probabilidades_5_primeros
print ''
print " <=4", probabilidades_4_primeros
print "  >4", 1-probabilidades_4_primeros

# Calculo orden
orden5 = np.argsort(-probabilidades_5_primeros)
probabilidades_5_primeros = probabilidades_5_primeros[orden5]
paises5 = np.asarray(list(collections.OrderedDict(sorted(paises.items())).keys()))[orden5]

orden4 = np.argsort(-probabilidades_4_primeros)
probabilidades_4_primeros = probabilidades_4_primeros[orden4]
paises4 = np.asarray(list(collections.OrderedDict(sorted(paises.items())).keys()))[orden4]

# Grafico
f, (ax0,ax1) = plt.subplots(2, 1, figsize=(10,6), sharex=False, sharey=True)
sns.barplot(paises5, np.ones(10), color=sns.xkcd_rgb["medium green"], ax=ax0, label='Queda entre los 5')
sns.barplot(paises5, 1-probabilidades_5_primeros, color=sns.xkcd_rgb["pale red"], ax=ax0, label='No queda entre los 5')
sns.barplot(paises4, np.ones(10), color=sns.xkcd_rgb["medium green"], ax=ax1, label='Queda entre los 4')
sns.barplot(paises4, 1-probabilidades_4_primeros, color=sns.xkcd_rgb["pale red"], ax=ax1, label='No queda entre los 4')
ax0.legend(ncol=1, frameon=True)
ax1.legend(ncol=1, frameon=True)
plt.setp(f.axes, yticks=np.arange(0,1.01,.1), xticks=np.arange(0,10))
plt.tight_layout(h_pad=2)
plt.show()
