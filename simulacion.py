import numpy as np

paises = {"Argentina":0, "Bolivia":1, "Brasil":2, "Chile":3, "Colombia":4,
        "Ecuador":5, "Paraguay":6, "Peru":7, "Uruguay":8, "Venezuela":9}

def simulacion(puntajes, probabilidades, iteraciones):
    posiciones = np.zeros((10,iteraciones),dtype=np.int)
    histograma = np.zeros((10,10))
    resultados = np.array([[3,0],[0,3],[1,1]]);

    # Obtengo partidos no jugados (los que la suma de puntajes da 0)
    no_jugados = np.nonzero(np.sum(puntajes, axis=2) == 0)

    for i in range(0,iteraciones):
        puntajes_copia = puntajes.copy()

        # Random ponderado en partidos no jugados
        for x in range(0,len(no_jugados[0])):
            if (no_jugados[0][x]!=no_jugados[1][x]):
                puntajes_copia[no_jugados[0][x],no_jugados[1][x]] = resultados[np.random.choice(3, 1, p = probabilidades[no_jugados[0][x],no_jugados[1][x]])]

        puntajes_local = np.sum(puntajes_copia, axis=1)[:,0]
        puntajes_visitante = np.sum(puntajes_copia, axis=0)[:,1]
        total = puntajes_local + puntajes_visitante
        posiciones[:,i] = np.lexsort((np.random.random(total.size), -np.array(total)))

    for i in range(0,10):
        histograma[i] = np.bincount(posiciones[i,:], minlength=10)

    # Normalizo histograma
    histograma = histograma / iteraciones
    
    return histograma

def getPais(index):
    for pais, i in paises.iteritems():
        if i == index:
            return pais

def getPuntajesIniciales():
    puntajes = np.zeros((10, 10, 2))

    # Partidos ya jugados
    puntajes[paises["Bolivia"],paises["Uruguay"]]=[0,3]
    puntajes[paises["Colombia"],paises["Peru"]]=[3,0]
    puntajes[paises["Venezuela"],paises["Paraguay"]]=[0,3]
    puntajes[paises["Chile"],paises["Brasil"]]=[3,0]
    puntajes[paises["Argentina"],paises["Ecuador"]]=[0,3]

    puntajes[paises["Ecuador"],paises["Bolivia"]]=[3,0]
    puntajes[paises["Uruguay"],paises["Colombia"]]=[3,0]
    puntajes[paises["Paraguay"],paises["Argentina"]]=[1,1]
    puntajes[paises["Brasil"],paises["Venezuela"]]=[3,0]
    puntajes[paises["Peru"],paises["Chile"]]=[0,3]

    puntajes[paises["Bolivia"],paises["Venezuela"]]=[3,0]
    puntajes[paises["Ecuador"],paises["Uruguay"]]=[3,0]
    puntajes[paises["Chile"],paises["Colombia"]]=[1,1]
    puntajes[paises["Argentina"],paises["Brasil"]]=[1,1]
    puntajes[paises["Peru"],paises["Paraguay"]]=[3,0]

    puntajes[paises["Colombia"],paises["Argentina"]]=[0,3]
    puntajes[paises["Venezuela"],paises["Ecuador"]]=[0,3]
    puntajes[paises["Uruguay"],paises["Chile"]]=[3,0]
    puntajes[paises["Paraguay"],paises["Bolivia"]]=[3,0]
    puntajes[paises["Brasil"],paises["Peru"]]=[3,0]

    return puntajes
