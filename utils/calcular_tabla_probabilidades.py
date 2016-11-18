#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import sqlite3

class Pais:
    Argentina   = 0
    Bolivia     = 1
    Brasil      = 2
    Chile       = 3
    Colombia    = 4
    Ecuador     = 5
    Paraguay    = 6
    Peru        = 7
    Uruguay     = 8
    Venezuela   = 9

def getPais(nombre):
    if nombre=="Argentina":
        return 0
    elif nombre=="Bolivia":
        return 1
    elif nombre=="Brasil":
        return 2
    elif nombre=="Chile":
        return 3
    elif nombre=="Colombia":
        return 4
    elif nombre=="Ecuador":
        return 5
    elif nombre=="Paraguay":
        return 6
    elif nombre=="Perú".decode('utf-8'):
        return 7
    elif nombre=="Uruguay":
        return 8
    elif nombre=="Venezuela":
        return 9

probabilidades_local = np.zeros((10,10))
probabilidades_visitante = np.zeros((10,10))
probabilidades_empate = np.zeros((10,10))

connection = sqlite3.connect('eliminatorias.db')
cursor = connection.cursor()
cursor.execute('select local,visitante,resultado from partidos where eliminatoria>=2006 order by local, visitante, eliminatoria')

factor = 0.7 # Porcentaje que incide el historico, el resto (1-factor) sera repartido de igual manera para local, visitante, empate.
f = round(((1-factor)/3),3)
r_l, r_e, r_v = 0, 0, 0
local, visitante = "", ""
for row in cursor:
    if ((local!=row[0]) | (visitante!=row[1])) &  (local!=""):
        r_t = r_l + r_e + r_v
        pv = f + round(factor * r_v/r_t,3)
        pe = f + round(factor * r_e/r_t,3)
        probabilidades_local[getPais(local),getPais(visitante)] = round(1 - pe - pv,3)
        probabilidades_visitante[getPais(local),getPais(visitante)] = pv
        probabilidades_empate[getPais(local),getPais(visitante)] = pe
        # print "%s - %s (%s,%s,%s,%s,%s,%s)" % (local,visitante,r_l,r_v,r_e,round(1 - pe - pv,3),pv,pe)
        r_l, r_e, r_v = 0, 0, 0

    local, visitante, resultado = row[0], row[1], row[2]
    if resultado=='L':
        r_l += 1
    elif resultado=='V':
        r_v += 1
    else:
        r_e += 1

r_t = r_l + r_e + r_v
pv = f + round(factor * r_v/r_t,3)
pe = f + round(factor * r_e/r_t,3)
probabilidades_local[getPais(local),getPais(visitante)] = round(1 - pe - pv,3)
probabilidades_visitante[getPais(local),getPais(visitante)] = pv
probabilidades_empate[getPais(local),getPais(visitante)] = pe
#print "%s - %s (%s,%s,%s,%s,%s,%s)" % (local,visitante,r_l,r_v,r_e,round(1 - pe - pv,3),pv,pe)

np.savetxt('local.out', probabilidades_local, fmt='%1.3f')
np.savetxt('visitante.out', probabilidades_visitante, fmt='%1.3f')
np.savetxt('empate.out', probabilidades_empate, fmt='%1.3f')

# Luego hacer: cat local.out visitante.out empate.out > probabilidades.txt
