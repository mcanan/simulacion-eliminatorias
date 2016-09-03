import math
import numpy as np
from collections import OrderedDict

PAISES = OrderedDict([("Argentina", 0), ("Bolivia", 1), ("Brasil", 2), ("Chile", 3), ("Colombia", 4), ("Ecuador", 5),
    ("Paraguay", 6), ("Peru", 7), ("Uruguay", 8), ("Venezuela", 9)])
POSIBLES_RESULTADOS = np.array([[3,0],[0,3],[1,1]]); # [gana local, gana visitante, empate]
RANGO_PUNTOS = np.arange(0,100)

def getPartidosNoJugados(puntajes):
    """
    Dada la matriz de puntajes devuelve los indices de los partidos que aun no se han jugado.
    """
    tmp = puntajes.copy()
    for i in range(0,len(tmp[0])):
        tmp[i,i,:] = [1,1]
    return np.nonzero(np.sum(tmp, axis=2) == 0)

def simularNoJugados(probabilidades, puntajes, no_jugados):
    """
    Simula los partidos que no se han jugado en la matriz de puntajes con las probabilidades dadas.
    Devuelve un array con los puntajes obtenidos al final por cada equipo.
    """
    # Random ponderado en partidos no jugados
    for x in range(0,len(no_jugados[0])):
        puntajes[no_jugados[0][x],no_jugados[1][x]] = POSIBLES_RESULTADOS[np.random.choice(3, 1, p = probabilidades[no_jugados[0][x],no_jugados[1][x]])]
    
    puntajes_local = np.sum(puntajes, axis=1)[:,0]
    puntajes_visitante = np.sum(puntajes, axis=0)[:,1]
    return puntajes_local + puntajes_visitante

def getHistogramaPuntos(puntajes, probabilidades, iteraciones):
    """
    Devuelve 3 histogramas no normalizados de la cantidad de ocurrencias por puntaje final por equipo.
    Los 3 histogramas estan dados por las 3 zonas de clasificacion (1-4,5,6-*).
    """
    cnt_equipos = puntajes.shape[0]
    posiciones = np.zeros((cnt_equipos, iteraciones), dtype=np.int)
    puntos = np.zeros((cnt_equipos, iteraciones), dtype=np.int)

    # Obtengo partidos no jugados (los que la suma de puntajes da 0)
    no_jugados = getPartidosNoJugados(puntajes)
    
    for i in range(0,iteraciones):
        puntajes_copia = puntajes.copy()
        puntaje_total = simularNoJugados(probabilidades, puntajes_copia, no_jugados)
        puntos[:,i] = puntaje_total
        posiciones[:,i] = np.lexsort((np.random.random(puntaje_total.size), -np.array(puntaje_total)))
    
    hist_zona0 = np.zeros((cnt_equipos, RANGO_PUNTOS.size-1), dtype=np.int)
    hist_zona1 = np.zeros((cnt_equipos, RANGO_PUNTOS.size-1), dtype=np.int)
    hist_zona2 = np.zeros((cnt_equipos, RANGO_PUNTOS.size-1), dtype=np.int)
    for i in range(0,cnt_equipos):
        p0 = np.where(posiciones[:4,:]==i) # Posicion 1-4
        p1 = np.where(posiciones[4:5,:]==i) # Posicion 5
        p2 = np.where(posiciones[5:,:]==i) # Posicion 6-* 
        hist_zona0[i,:] = np.histogram(puntos[i, p0[1]],bins=RANGO_PUNTOS)[0]
        hist_zona1[i,:] = np.histogram(puntos[i, p1[1]],bins=RANGO_PUNTOS)[0]
        hist_zona2[i,:] = np.histogram(puntos[i, p2[1]],bins=RANGO_PUNTOS)[0]

    return hist_zona0, hist_zona1, hist_zona2

def getHistogramaPosiciones(puntajes, probabilidades, iteraciones):
    """
    Devuelve un histograma normalizado de la cantidad de ocurrencias en cada posicion de la tabla final por equipo.
    """
    cnt_equipos = puntajes.shape[0]
    posiciones = np.zeros((cnt_equipos, iteraciones), dtype=np.int)
    histograma = np.zeros((cnt_equipos, cnt_equipos))

    # Obtengo partidos no jugados (los que la suma de puntajes da 0)
    no_jugados = getPartidosNoJugados(puntajes)

    for i in range(0,iteraciones):
        puntajes_copia = puntajes.copy()
        puntaje_total = simularNoJugados(probabilidades, puntajes_copia, no_jugados)
        posiciones[:,i] = np.lexsort((np.random.random(puntaje_total.size), -np.array(puntaje_total)))

    for i in range(0, cnt_equipos):
        histograma[i] = np.bincount(posiciones[i,:], minlength=cnt_equipos)

    # Normalizo
    histograma = histograma / iteraciones

    return histograma

def getProbabilidades(archivo):
    """
    Carga desde un archivo las probabilidades de resultados de cada partido.
    """
    probabilidades = np.loadtxt(archivo)
    probabilidades = np.reshape(probabilidades.T, (probabilidades.shape[0]/3, probabilidades.shape[0]/3, 3), order='F')
    probabilidades = np.swapaxes(probabilidades, 0, 1)

    return probabilidades

def getPuntajesIniciales(fecha):
    """
    Devuelve la matriz de puntajes con los resultados reales cargados hasta la fecha dada inclusive.
    """
    partidos = getPartidosJugados()
    puntajes = np.zeros((10, 10, 2))

    partidos_hasta_la_fecha = (partidos[:,:,0]>0) & (partidos[:,:,0]<=fecha) 
    partidos_gana_local = (partidos[:,:,1]>partidos[:,:,2]) & partidos_hasta_la_fecha
    partidos_gana_visitante = (partidos[:,:,2]>partidos[:,:,1]) & partidos_hasta_la_fecha
    partidos_empate = (partidos[:,:,1]==partidos[:,:,2]) & partidos_hasta_la_fecha
   
    puntajes[partidos_gana_local]=[3,0]
    puntajes[partidos_gana_visitante]=[0,3]
    puntajes[partidos_empate]=[1,1]
    
    return puntajes

def getPartido(fecha, pais):
    """
    Dada una fecha y un pais devuelve un string con el resultado del partido del pais para esa fecha.
    """
    if (fecha<1):
        return ''

    partidos = getPartidosJugados()
    pais_visitante = (partidos[pais,:,0]==fecha)
    pais_local = (partidos[:,pais,0]==fecha)
    if (pais_visitante.any()):
        id_pais_visitante = np.where(pais_visitante==True)[0][0]
        pl = PAISES.items()[pais][0][:3].upper()
        pv = PAISES.items()[id_pais_visitante][0][:3].upper()
        resultado = '%d'%(partidos[pais, id_pais_visitante,1:][0]) + ' - ' + '%d'%(partidos[pais, id_pais_visitante,1:][1])
    elif (pais_local.any()):
        id_pais_local = np.where(pais_local==True)[0][0]
        pl = PAISES.items()[id_pais_local][0][:3].upper()
        pv = PAISES.items()[pais][0][:3].upper()
        resultado = '%d'%(partidos[id_pais_local, pais,1:][0]) + ' - ' + '%d'%(partidos[id_pais_local, pais,1:][1])
    else:
        return ''
    return pl + ' ' + resultado + ' ' + pv

def getPartidosJugados():
    """
    Devuelve la matriz de partidos reales ya jugados.
    """
    partidos = np.zeros((10, 10, 3)) # Local, Visitante, , (fecha, goles local, goles visitante)

    # Fecha 1
    partidos[PAISES["Bolivia"],PAISES["Uruguay"]]=[1,0,2]
    partidos[PAISES["Colombia"],PAISES["Peru"]]=[1,2,0]
    partidos[PAISES["Venezuela"],PAISES["Paraguay"]]=[1,0,1]
    partidos[PAISES["Chile"],PAISES["Brasil"]]=[1,2,0]
    partidos[PAISES["Argentina"],PAISES["Ecuador"]]=[1,0,2]

    # Fecha 2
    partidos[PAISES["Ecuador"],PAISES["Bolivia"]]=[2,2,0]
    partidos[PAISES["Uruguay"],PAISES["Colombia"]]=[2,3,0]
    partidos[PAISES["Paraguay"],PAISES["Argentina"]]=[2,0,0]
    partidos[PAISES["Brasil"],PAISES["Venezuela"]]=[2,3,1]
    partidos[PAISES["Peru"],PAISES["Chile"]]=[2,3,4]

    # Fecha 3
    partidos[PAISES["Bolivia"],PAISES["Venezuela"]]=[3,4,2]
    partidos[PAISES["Ecuador"],PAISES["Uruguay"]]=[3,2,1]
    partidos[PAISES["Chile"],PAISES["Colombia"]]=[3,1,1]
    partidos[PAISES["Argentina"],PAISES["Brasil"]]=[3,1,1]
    partidos[PAISES["Peru"],PAISES["Paraguay"]]=[3,1,0]

    # Fecha 4
    partidos[PAISES["Colombia"],PAISES["Argentina"]]=[4,0,1]
    partidos[PAISES["Venezuela"],PAISES["Ecuador"]]=[4,1,3]
    partidos[PAISES["Uruguay"],PAISES["Chile"]]=[4,3,0]
    partidos[PAISES["Paraguay"],PAISES["Bolivia"]]=[4,2,1]
    partidos[PAISES["Brasil"],PAISES["Peru"]]=[4,3,0]

    # Fecha 5
    partidos[PAISES["Bolivia"],PAISES["Colombia"]]=[5,2,3]
    partidos[PAISES["Ecuador"],PAISES["Paraguay"]]=[5,2,2]
    partidos[PAISES["Chile"],PAISES["Argentina"]]=[5,1,2]
    partidos[PAISES["Peru"],PAISES["Venezuela"]]=[5,2,2]
    partidos[PAISES["Brasil"],PAISES["Uruguay"]]=[5,2,2]

    # Fecha 6
    partidos[PAISES["Colombia"],PAISES["Ecuador"]]=[6,3,1]
    partidos[PAISES["Uruguay"],PAISES["Peru"]]=[6,1,0]
    partidos[PAISES["Argentina"],PAISES["Bolivia"]]=[6,2,0]
    partidos[PAISES["Venezuela"],PAISES["Chile"]]=[6,1,4]
    partidos[PAISES["Paraguay"],PAISES["Brasil"]]=[6,2,2]

    # Fecha 7
    partidos[PAISES["Bolivia"],PAISES["Peru"]]=[7,2,0]
    partidos[PAISES["Colombia"],PAISES["Venezuela"]]=[7,2,0]
    partidos[PAISES["Ecuador"],PAISES["Brasil"]]=[7,0,3]
    partidos[PAISES["Argentina"],PAISES["Uruguay"]]=[7,1,0]
    partidos[PAISES["Paraguay"],PAISES["Chile"]]=[7,2,1]

    return partidos
