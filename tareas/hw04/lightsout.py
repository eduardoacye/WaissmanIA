#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'nombre del estudiante'


from busquedas import *
import math
import heapq


class Lights_out(ProblemaBusqueda):
#---------------------------------------------------------------
# Problema 1 (25 puntos): Desarrolla la clase para el problema de lights out
#
#---------------------------------------------------------------

    """
    Problema del jueguito "Ligths out".

    La idea del juego es el apagar todas las luces.
    Al seleccionar una casilla, la casilla y sus casillas adjacentes cambian
    (si estan prendidas se apagan y viceversa). El juego consiste en una matriz
    de 5 X 5, cuyo estado puede ser apagado 0 o prendido 1. Por ejemplo el estado

       (0,0,1,0,0,1,1,0,0,1,0,0,1,1,0,1,0,1,0,1,0,0,0,0,0)

    corresponde a:

    ---------------------
    |   |   | X |   |   |
    ---------------------
    | X | X |   |   | X |
    ---------------------
    |   |   | X | X |   |
    ---------------------
    | X |   | X |   | X |
    ---------------------
    |   |   |   |   |   |
    ---------------------
    
    Las acciones posibles son de elegir cambiar una luz y sus casillas adjacentes, por lo que la accion es
    un número entre 0 y 24.

    Para mas información sobre el juego, se puede consultar

    http://en.wikipedia.org/wiki/Lights_Out_(game)

    """
    def __init__(self, pos_inicial):
        def meta(s):
            return all(map(lambda x: x==0, s))
            
        super(Lights_out, self).__init__(pos_inicial, meta)


    def acciones_legales(self, estado):
        return range(25)

    def sucesor(self, estado, accion):
        def switch(e, i):
            if e[i] == 0:
                e[i] = 1
            else:
                e[i] = 0

        s = list(estado)
        switch(s,accion)
        if accion > 4:
            switch(s,accion-5)
        if accion < 20:
            switch(s,accion+5)
        if accion%5 < 4:
            switch(s,accion+1)
        if accion%5 > 0:
            switch(s,accion-1)
        return tuple(s)


    def costo_local(self, estado, accion):
        return 1

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        cadena = "---------------------\n"
        for i in range(5):
            for j in range(5):
                if estado[5 * i + j]:
                    cadena += "| X "
                else:
                    cadena += "|   "
            cadena += "|\n---------------------\n"
        return cadena

class Lights_out_relajado(Lights_out):
    def __init__(self, pos_inicial):
        super(Lights_out_relajado, self).__init__(pos_inicial)

    def sucesor(self, estado, accion):
        def switch(e, i):
            if e[i] == 0:
                e[i] = 1
            else:
                e[i] = 0

        s = list(estado)
        switch(s,accion)

        if accion > 4:
            s[accion-5] = 0
        if accion < 20:
            s[accion+5] = 0
        if accion%5 < 4:
            s[accion+1] = 0
        if accion%5 > 0:
            s[accion-1] = 0

        return tuple(s)


#-------------------------------------------------------------------------------------------------
# Problema 2 (25 puntos): Desarrolla el método de búsqueda de A* siguiendo las especificaciones de la función 
#
# RESUELVE ESTE PROBLEMA EN EL OCHO_PUZZLE Y LUEGO SIMPLEMENTE COPIALA, YA QUE LAS HEURÍSTICAS SON 
# MUY DIFICILES PARA ESTE PROBLEMA
#-------------------------------------------------------------------------------------------------
def busqueda_A_estrella(problema, heuristica):
    """
    Búsqueda A*

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda
    @param heuristica: Una funcion de heuristica, esto es, una función heuristica(nodo), la cual devuelva
                       un número mayor o igual a cero con el costo esperado desde nodo hasta un nodo 
                       objetivo.

    @return Un objeto tipo Nodo con la estructura completa

    
    """
    frontera = []
    heapq.heappush(frontera, (heuristica(Nodo(problema.s0)), Nodo(problema.s0)))
    visitados = {problema.s0: heuristica(Nodo(problema.s0))}

    while frontera:
        (_, nodo) = heapq.heappop(frontera)
        if problema.es_meta(nodo.estado):
            nodo.nodos_visitados = problema.num_nodos
            return nodo
        for hijo in nodo.expande(problema):
            fn = hijo.costo + heuristica(hijo)
            if hijo.estado not in visitados or visitados[hijo.estado] > fn:
                heapq.heappush(frontera, (fn, hijo))
                visitados[hijo.estado] = fn

    return None


def prueba_clase():
    """
    Prueba la clase Lights_out
    
    """
    
    
    pos_ini = (0, 1, 0, 1, 0,
               0, 0, 1, 1, 0,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1)

    pos_a0 =  (1, 0, 0, 1, 0,
               1, 0, 1, 1, 0,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1)

    pos_a4 =  (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1)

    pos_a24 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 0,
               0, 0, 0, 0, 0)

    pos_a15 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 1, 0,
               1, 0, 0, 0, 0)

    pos_a12 = (1, 0, 0, 0, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 0, 1,
               1, 1, 0, 1, 0,
               1, 0, 0, 0, 0)


    entorno = Lights_out(pos_ini)

    assert entorno.acciones_legales(pos_ini) == range(25)
    assert entorno.sucesor(pos_ini, 0) == pos_a0
    assert entorno.sucesor(pos_a0, 4) == pos_a4
    assert entorno.sucesor(pos_a4, 24) == pos_a24
    assert entorno.sucesor(pos_a24, 15) == pos_a15
    assert entorno.sucesor(pos_a15, 12) == pos_a12
    print "Paso la prueba de la clase"
    

def prueba_busqueda(pos_inicial, metodo, heuristica=None, max_prof=None):
    """
    Prueba un método de búsqueda para el problema del ligths out.

    @param pos_inicial: Una tupla con una posicion inicial
    @param metodo: Un metodo de búsqueda a probar
    @param heuristica: Una función de heurística, por default None si el método de búsqueda no requiere heuristica
    @param max_prof: Máxima profundidad para los algoritmos de DFS y IDS.

    @return nodo: El nodo solución

    """
    if heuristica:
        return metodo(Lights_out(pos_inicial), heuristica)
    elif max_prof:
        return metodo(Lights_out(pos_inicial), max_prof)
    else:
        return metodo(Lights_out(pos_inicial))


def compara_metodos(pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución de varios métodos de búsqueda

    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    @return None (no regresa nada, son puros efectos colaterales)

    Si la búsqueda no informada es muy lenta, posiblemente tendras que quitarla de la función
    """
    #n1 = prueba_busqueda(pos_inicial, busqueda_ancho)
    #n2 = prueba_busqueda(pos_inicial, busqueda_profundidad_iterativa)
    #n3 = prueba_busqueda(pos_inicial, busqueda_costo_uniforme)
    n4 = prueba_busqueda(pos_inicial, busqueda_A_estrella, heuristica_1)
    #n5 = prueba_busqueda(pos_inicial, busqueda_A_estrella, heuristica_2)

    print '\n\n' + '-' * 50
    print u'Método'.center(10) + 'Costo de la solucion'.center(20) + 'Nodos explorados'.center(20)
    print '-' * 50
    #print 'BFS'.center(10) + str(n1.costo).center(20) + str(n1.nodos_visitados)
    #print 'IDS'.center(10) + str(n2.costo).center(20) + str(n2.nodos_visitados)
    #print 'UCS'.center(10) + str(n3.costo).center(20) + str(n3.nodos_visitados)
    print 'A* con h1'.center(10) + str(n4.costo).center(20) + str(n4.nodos_visitados)
    #print 'A* con h2'.center(10) + str(n5.costo).center(20) + str(n5.nodos_visitados)
    print ''
    print '-' * 50 + '\n\n'

if __name__ == "__main__":

    print "Antes de hacer otra cosa vamos a verificar medianamente la clase Lights_out"
    prueba_clase()



#-------------------------------------------------------------------------------------------------
# Problema 3 (25 puntos): Desarrolla una política admisible. 
#-------------------------------------------------------------------------------------------------
    def h_1(nodo):
        """
        DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN PLATICADA DE PORQUÉ CREES QUE
        LA HEURÍSTICA ES ADMISIBLE

        """
        """
        # Esta primer heuristica es bastante macana y es bien parecida a la que respondi en el
        # examen:
        #
        # El techo de: la cantidad de 1's / 5.0
        #
        # Es admisible ya que la maxima cantidad de celdas que cambiaran de color en una sola
        # accion es 5. Conforme nos acerquemos a la solucion, la cantidad de celdas de un valor
        # en particular disminuye hasta que falte un turno
        estado = nodo.estado
        ceros = len(filter(lambda x: x==0, estado))
        unos = len(filter(lambda x: x==1, estado))
        if ceros < unos:
            return math.ceil(ceros/5.0)
        return math.ceil(unos/5.0)
        """
        
        estado = nodo.estado
        return math.ceil(len(filter(lambda x: x==1, estado))/5.0)
        

#-------------------------------------------------------------------------------------------------
# Problema 4 (25 puntos): Desarrolla otra política admisible. 
# Analiza y di porque piensas que es (o no es) dominante una respecto otra política
#-------------------------------------------------------------------------------------------------
    def h_2(nodo):
        """
        DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN PLATICADA DE PORQUÉ CREES QUE
        LA HEURÍSTICA ES ADMISIBLE

        """
        #
        # Realizar una busqueda A* desde nodo hasta el nodo meta con un problema relajado
        #
        # Es admisible ya que en cualquier configuracion se llega a la solucion en igual o menos pasos que
        # con el problema no relajado (ya que en lugar de "switchear" celdas, solo se "apagan").
        #
        #
        #
        # Para que una heuristica h_a sea dominante sobre otra h_b, se tiene que cumplir que para todo nodo
        # n, h_a(n) >= h_b(n). Lo que cuenta h_1 es la cantidad de celdas prendidas, esta cantidad es divi-
        # dida sobre 5, por lo tanto siempre sera menor o igual al costo hacia delante con un problema re-
        # lajado de la h_2 ya que si en el peor de los casos h_2 resulta en x, h_1 resultara x/5, mientras que
        # en el mejor de los casos, si h_2 resulta x', h_1 resulta en x'.
        #
        # A pesar de que h_2 es dominante sobre h_1, el tiempo de ejecucion es mas rapido con h_1,

        n = busqueda_A_estrella(Lights_out_relajado(nodo.estado), h_1)
        return n.costo

    diagonal = (0, 0, 0, 0, 1,
                0, 0, 0, 1, 0,
                0, 0, 1, 0, 0,
                0, 1, 0, 0, 0,
                1, 0, 0, 0, 0)

    simetria = (1, 0, 1, 0, 1,
                1, 0, 1, 0, 1,
                0, 0, 0, 0, 0,
                1, 0, 1, 0, 1,
                1, 0, 1, 0, 1)

    problemin = (0, 1, 0, 1, 0,
                 0, 0, 1, 1, 0,
                 0, 0, 0, 1, 1,
                 0, 0, 1, 1, 1,
                 0, 0, 0, 1, 1)

    print u"\n\nVamos a ver como funcionan las búsquedas para un estado inicial"
    print "\n" + Lights_out.bonito(diagonal)
    compara_metodos(diagonal, h_1, h_2)

    print u"\n\nVamos a ver como funcionan las búsquedas para un estado inicial"
    print "\n" + Lights_out.bonito(simetria)
    compara_metodos(simetria, h_1, h_2)
    
    print u"\n\nVamos a ver como funcionan las búsquedas para un estado inicial"
    print "\n" + Lights_out.bonito(problemin)
    compara_metodos(problemin, h_1, h_2)
    