import numpy as np
import matplotlib.pyplot as plt
from simulacion import *

probabilidades = getProbabilidades('probabilidades.txt')
puntos = np.arange(5,43)

sum_z1 = np.zeros((len(PAISES)), dtype=np.float)
sum_z2 = np.zeros((len(PAISES)), dtype=np.float)
sum_z3 = np.zeros((len(PAISES)), dtype=np.float)
for fecha in range(7): # 7
    # Inicializo matrices
    puntajes = getPuntajesIniciales(fecha)
    hz0, hz1, hz2 = getHistogramaPuntos(puntajes, probabilidades, 100) # Corro con 30000 iteraciones.

    # Grafico
    plt.style.use('ggplot')
    plt.figure(figsize=(15,20))
    for pais in PAISES.items():
        i = pais[1]
        htotal=hz0[i]+hz1[i]+hz2[i]
        z1 = np.divide(hz0[i], np.sum(htotal), dtype=float)
        z2 = np.divide(hz1[i], np.sum(htotal), dtype=float)
        z3 = np.divide(hz2[i], np.sum(htotal), dtype=float)
        p = np.divide(htotal, np.sum(htotal), dtype=float)
        ax = plt.subplot(len(PAISES), 1, i+1)
        plt.axis([10, 35, 0, 0.15])
        ax.set_xticks(puntos)
        ax.set_axis_bgcolor((0.9, 0.9, 0.9))
        ax.set_yticks([0,0.05,0.1])
        ax.set_title(pais[0], x=0.03, y=0.7, loc='left')

        z1r = round(np.sum(z1),2)
        z2r = round(np.sum(z2),2)
        z3r = (1 - z1r - z2r) # Para que sume 1. Deberia ser round(np.sum(z2),2)
        ax.text(0.99, 0.85, getPartido(fecha,i), transform=ax.transAxes, color='#aaaaaa', fontsize=11, horizontalalignment='right')
        ax.text(0.89, 0.70, '%.2f'%(z1r), transform=ax.transAxes, color='#2ecc71', fontsize=11, horizontalalignment='right')
        ax.text(0.94, 0.70, '%.2f'%(z2r), transform=ax.transAxes, color='#f39c12', fontsize=11, horizontalalignment='right')
        ax.text(0.99, 0.70, '%.2f'%(z3r), transform=ax.transAxes, color='#e74c3c', fontsize=11, horizontalalignment='right')
        if (fecha>0):
            ax.text(0.89, 0.55, '%+.2f'%(z1r - sum_z1[i]), transform=ax.transAxes, color='#aaaaaa', fontsize=11, horizontalalignment='right')
            ax.text(0.94, 0.55, '%+.2f'%(z2r - sum_z2[i]), transform=ax.transAxes, color='#aaaaaa', fontsize=11, horizontalalignment='right')
            ax.text(0.99, 0.55, '%+.2f'%(z3r - sum_z3[i]), transform=ax.transAxes, color='#aaaaaa', fontsize=11, horizontalalignment='right')
            sum_z1[i] = z1r
            sum_z2[i] = z2r
            sum_z3[i] = z3r
                                                                                                                                                                                                                                                                            
            ax.set_axis_bgcolor("#f4f4f4")
            rects1 = ax.bar(puntos, (z1+z2+z3)[puntos], 0.8, color="#2ecc71", align='center')
            rects1 = ax.bar(puntos, (z2+z3)[puntos], 0.8, color="#f39c12", align='center')
            rects1 = ax.bar(puntos, z3[puntos], 0.8, color="#e74c3c", align='center')
            plt.savefig('f'+str(fecha)+'.png', bbox_inches='tight')
