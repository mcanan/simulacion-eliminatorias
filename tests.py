import unittest
from simulacion import *

class TestSimulacion(unittest.TestCase):

    def test_sum1(self):
        probabilidades = getProbabilidades('probabilidades.txt')
        test = np.ones((10,10)) - np.identity(10)
        tmp = np.round(np.sum(probabilidades, axis=2),5)
        np.testing.assert_equal(tmp, test)

    def test_getProbabilidades(self):
        probabilidades = getProbabilidades('tests/test_probabilidades.txt')
        p0 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        p1 = np.array([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
        p2 = np.array([[19, 20, 21], [22, 23, 24], [25, 26, 27]])
        np.testing.assert_equal(probabilidades[:,:,0], p0)
        np.testing.assert_equal(probabilidades[:,:,1], p1)
        np.testing.assert_equal(probabilidades[:,:,2], p2)

    def test_simularNoJugados(self):
        probabilidades = getProbabilidades('tests/test_simulacion.txt')

        puntajes = np.zeros((3, 3, 2))
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 6)
        puntajes_total = simularNoJugados(probabilidades, puntajes, no_jugados)
        p = np.array([9, 7, 1])
        np.testing.assert_equal(puntajes_total, p)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 0)

        puntajes = np.zeros((3, 3, 2))
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 6)
        puntajes[2,1]=[0,3]
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 5)
        puntajes_total = simularNoJugados(probabilidades, puntajes, no_jugados)
        p = np.array([9, 9, 0])
        np.testing.assert_equal(puntajes_total, p)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 0)

        puntajes = np.zeros((3, 3, 2))
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 6)
        puntajes[2,1]=[0,3]
        puntajes[1,0]=[0,3]
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 4)
        puntajes_total = simularNoJugados(probabilidades, puntajes, no_jugados)
        p = np.array([12, 6, 0])
        np.testing.assert_equal(puntajes_total, p)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 0)

    def test_getPartidosNoJugados(self):
        puntajes = np.zeros((3, 3, 2))
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size,6)
        
        puntajes = np.zeros((3, 3, 2))
        puntajes[2,0]=[3,0]
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size,5)

        puntajes = np.zeros((3, 3, 2))
        puntajes[2,0]=[3,0]
        puntajes[1,0]=[1,1]
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size,4)

        puntajes = np.zeros((3, 3, 2))
        puntajes[2,0]=[3,0]
        puntajes[1,0]=[1,1]
        puntajes[1,2]=[0,0]
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size,4)

    def test_getHistogramaPorPuntos(self):
        puntajes = np.zeros((3, 3, 2))
        probabilidades = getProbabilidades('tests/test_histograma.txt')
        hz0, hz1, hz2 = getHistogramaPuntos(puntajes, probabilidades, 3000)
        htotal = hz0[0] + hz1[0] + hz2[0]
        puntos = np.nonzero(htotal)
        z1 = np.divide(hz0[0][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)
        z2 = np.divide(hz1[0][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)
        z3 = np.divide(hz2[0][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)
        prc = np.divide(htotal[np.nonzero(htotal)], np.sum(htotal[np.nonzero(htotal)]), dtype=float)
        p = np.array([7, 9])
        np.testing.assert_equal(puntos[0], p)
        self.assertTrue(prc[0]>0.35)
        self.assertTrue(prc[0]<0.45)
        self.assertTrue(prc[1]>0.55)
        self.assertTrue(prc[1]<0.65)

        puntajes = np.zeros((3, 3, 2))
        probabilidades = getProbabilidades('tests/test_histograma.txt')
        hz0, hz1, hz2 = getHistogramaPuntos(puntajes, probabilidades, 3000)
        htotal = hz0[2] + hz1[2] + hz2[2]
        puntos = np.nonzero(htotal)
        z1 = np.divide(hz0[2][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)
        z2 = np.divide(hz1[2][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)
        z3 = np.divide(hz2[2][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)
        prc = np.divide(htotal[np.nonzero(htotal)], np.sum(htotal[np.nonzero(htotal)]), dtype=float)
        p = np.array([0, 1, 2])
        np.testing.assert_equal(puntos[0], p)
        self.assertTrue(prc[0]>0.25)
        self.assertTrue(prc[0]<0.35)
        self.assertTrue(prc[1]>0.45)
        self.assertTrue(prc[1]<0.55)
        self.assertTrue(prc[2]>0.15)
        self.assertTrue(prc[2]<0.25)
        
        puntajes = np.zeros((10, 10, 2))
        probabilidades = getProbabilidades('tests/test_histograma_2.txt')
        hz0, hz1, hz2 = getHistogramaPuntos(puntajes, probabilidades, 3000)
        htotal = hz0[0] + hz1[0] + hz2[0]
        puntos = np.nonzero(htotal)
        z1 = np.divide(hz0[0][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)
        z2 = np.divide(hz1[0][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)
        z3 = np.divide(hz2[0][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)
        prc = np.divide(htotal[np.nonzero(htotal)], np.sum(htotal[np.nonzero(htotal)]), dtype=float)
        p = np.array([35, 38, 41])
        np.testing.assert_equal(puntos[0], p)
        self.assertTrue(prc[0]>0.20)
        self.assertTrue(prc[0]<0.30)
        self.assertTrue(prc[1]>0.45)
        self.assertTrue(prc[1]<0.55)
        self.assertTrue(prc[2]>0.20)
        self.assertTrue(prc[2]<0.30)
        
        puntajes = np.zeros((10, 10, 2))
        probabilidades = getProbabilidades('tests/test_histograma_2.txt')
        hz0, hz1, hz2 = getHistogramaPuntos(puntajes, probabilidades, 3000)
        htotal = hz0[8] + hz1[8] + hz2[8]
        puntos = np.nonzero(htotal)
        z1 = np.divide(hz0[8][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)
        z2 = np.divide(hz1[8][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)
        z3 = np.divide(hz2[8][np.nonzero(htotal)],htotal[np.nonzero(htotal)], dtype=float)
        prc = np.divide(htotal[np.nonzero(htotal)], np.sum(htotal[np.nonzero(htotal)]), dtype=float)
        p = np.array([17, 19])
        np.testing.assert_equal(puntos[0], p)
        self.assertTrue(prc[0]>0.35)
        self.assertTrue(prc[0]<0.45)
        self.assertTrue(prc[1]>0.55)
        self.assertTrue(prc[1]<0.65)

    def test_getHistogramaPorPosicion(self):
        puntajes = np.zeros((3, 3, 2))
        probabilidades = getProbabilidades('tests/test_histograma.txt')
        histograma = getHistogramaPosiciones(puntajes, probabilidades, 3000)
        self.assertTrue(histograma[0,0]>histograma[1,0])
        self.assertTrue(histograma[0,0]>0.52)
        self.assertTrue(histograma[1,0]<0.48)
        self.assertEqual(histograma[2,2],1)
        
        puntajes = np.zeros((3, 3, 2))
        puntajes[2,0]=[3,0]
        histograma = getHistogramaPosiciones(puntajes, probabilidades, 100)
        self.assertEqual(histograma[0,1],1)
        self.assertEqual(histograma[1,0],1)
        self.assertEqual(histograma[2,2],1)
        
        puntajes = np.zeros((3, 3, 2))
        puntajes[2,0]=[3,0]
        puntajes[2,1]=[3,0]
        histograma = getHistogramaPosiciones(puntajes, probabilidades, 2000)
        self.assertTrue(histograma[0,0]>0.3)
        self.assertTrue(histograma[1,0]>0.3)
        self.assertTrue(histograma[2,0]>0.3)

    def test_getPuntajesIniciales(self):
        # ARG BOL BRA CHI COL ECU PAR PER URU VEN
        puntajes = getPuntajesIniciales(1)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 85)
        puntajes_total = np.sum(puntajes, axis=1)[:,0] + np.sum(puntajes, axis=0)[:,1]
        p = np.array([0, 0, 0, 3, 3, 3, 3, 0, 3, 0])
        np.testing.assert_equal(puntajes_total, p)

        puntajes = getPuntajesIniciales(2)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 80)
        puntajes_total = np.sum(puntajes, axis=1)[:,0] + np.sum(puntajes, axis=0)[:,1]
        p = np.array([1, 0, 3, 6, 3, 6, 4, 0, 6, 0])
        np.testing.assert_equal(puntajes_total, p)

        puntajes = getPuntajesIniciales(3)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 75)
        puntajes_total = np.sum(puntajes, axis=1)[:,0] + np.sum(puntajes, axis=0)[:,1]
        p = np.array([2, 3, 4, 7, 4, 9, 4, 3, 6, 0])
        np.testing.assert_equal(puntajes_total, p)

        puntajes = getPuntajesIniciales(4)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 70)
        puntajes_total = np.sum(puntajes, axis=1)[:,0] + np.sum(puntajes, axis=0)[:,1]
        p = np.array([5, 3, 7, 7, 4, 12, 7, 3, 9, 0])
        np.testing.assert_equal(puntajes_total, p)

        puntajes = getPuntajesIniciales(5)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 65)
        puntajes_total = np.sum(puntajes, axis=1)[:,0] + np.sum(puntajes, axis=0)[:,1]
        p = np.array([8, 3, 8, 7, 7, 13, 8, 4, 10, 1])
        np.testing.assert_equal(puntajes_total, p)

        puntajes = getPuntajesIniciales(6)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 60)
        puntajes_total = np.sum(puntajes, axis=1)[:,0] + np.sum(puntajes, axis=0)[:,1]
        p = np.array([11, 3, 9, 10, 10, 13, 9, 4, 13, 1])
        np.testing.assert_equal(puntajes_total, p)

        # ARG BOL BRA CHI COL ECU PAR PER URU VEN
        puntajes = getPuntajesIniciales(7)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 55)
        puntajes_total = np.sum(puntajes, axis=1)[:,0] + np.sum(puntajes, axis=0)[:,1]
        p = np.array([14, 3, 12, 10, 13, 13, 12, 7, 13, 1])
        np.testing.assert_equal(puntajes_total, p)
        
        puntajes = getPuntajesIniciales(8)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 50)
        puntajes_total = np.sum(puntajes, axis=1)[:,0] + np.sum(puntajes, axis=0)[:,1]
        p = np.array([15, 3, 15, 13, 13, 13, 12, 10, 16, 2])
        np.testing.assert_equal(puntajes_total, p)
        
        puntajes = getPuntajesIniciales(9)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 45)
        puntajes_total = np.sum(puntajes, axis=1)[:,0] + np.sum(puntajes, axis=0)[:,1]
        p = np.array([16, 3, 18, 13, 16, 16, 12, 11, 19, 2])
        np.testing.assert_equal(puntajes_total, p)
        
        puntajes = getPuntajesIniciales(10)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 40)
        puntajes_total = np.sum(puntajes, axis=1)[:,0] + np.sum(puntajes, axis=0)[:,1]
        p = np.array([16, 4, 21, 16, 17, 17, 15, 11, 20, 2])
        np.testing.assert_equal(puntajes_total, p)
        
        puntajes = getPuntajesIniciales(11)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 35)
        puntajes_total = np.sum(puntajes, axis=1)[:,0] + np.sum(puntajes, axis=0)[:,1]
        p = np.array([16, 4, 24, 17, 18, 17, 15, 14, 23, 5])
        np.testing.assert_equal(puntajes_total, p)
        
        puntajes = getPuntajesIniciales(12)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 30)
        puntajes_total = np.sum(puntajes, axis=1)[:,0] + np.sum(puntajes, axis=0)[:,1]
        p = np.array([19, 7, 27, 20, 18, 20, 15, 14, 23, 5])
        np.testing.assert_equal(puntajes_total, p)
        # ARG BOL BRA CHI COL ECU PAR PER URU VEN

        puntajes = getPuntajesIniciales(13)
        no_jugados = getPartidosNoJugados(puntajes)
        self.assertEqual(no_jugados[0].size, 25)
        puntajes_total = np.sum(puntajes, axis=1)[:,0] + np.sum(puntajes, axis=0)[:,1]
        p = np.array([22, 7, 30, 20, 21, 20, 18, 15, 23, 6])
        np.testing.assert_equal(puntajes_total, p)
        # ARG BOL BRA CHI COL ECU PAR PER URU VEN
if __name__ == '__main__':
    unittest.main()
