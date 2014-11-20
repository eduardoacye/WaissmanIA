#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
dos_botes.py
------------

Ejemplo de problema de búsqueda, los dos botes

"""

__author__ = 'juliowaissman'

import busquedas


class PbDosBotes(busquedas.ProblemaBusqueda):
    """
    Problema de los dos botes:

    En este problema se tienen dos botes de diferente capacidad, un grifo y un resumidero.

    Se asume que las únicas acciones posibles a realizar son llenar los botes, vaciar los botes
    (uno solo a la vez) o transvasar liquido de uno a otro, solo hasta que uno esté vacio o el otro lleno.

    El problema es encontrar el núero mínimo de pasos para que al final un bote tenga la cantidad de
    agua deseada (cualquiera de ellos).

    """

    def __init__(self, maxA, maxB, meta):
        """
        Inicializa el entorno.
        
        @param maxA: Entero positivo con la máxima capacidad del bote A
        @param maxB: Entero positivo con la máxima capacidad del bote B
        @param meta: Entero entre 1 y max(maxA, maxB) con la cantidad deseada en uno de los botes.
            
        El estado del sistema es la tupla (a, b) donde a es la cantidad de agua en el bote 0, 
        y b es la cantidad de agua en el bote 1.
        
        El costo de las operaciones es de 1 por cada acción realizada
            
        """
        super(PbDosBotes, self).__init__((0, 0), lambda s: meta in s)
        self.limites = [maxA, maxB]

    def acciones_legales(self, estado):
        """
        Devuelve las acciones legales para un estado legal dado.
        
        @param estado: Un estado dado por la tupla (a, b)
        
        @return: Una lista de acciones legales en el estado
        
        Las acciones posibles son:
            ('llenar', 0), ('llenar', 1), ('vaciar', 0), ('vaciar', 1), ('pasar', 0, 1), ('pasar', 1, 0).
        
        La manera en que está programado el problema está lejos de ser optima pero es la más clara desde un punto de vista
        didáctico segun yo.
        
        """
        acciones = []
        for bote in range(2):
            if estado[bote] < self.limites[bote]:
                acciones.append(('llenar', bote))
            if estado[bote] > 0:
                acciones.append(('vaciar', bote))
                if estado[1-bote] < self.limites[1-bote]:
                    acciones.append(('pasar', bote, 1-bote))
        return acciones            
        
        # Si quieres la versión funcional, aunque un poco menos clara solo comenta todo lo de arriba
        # y descomenta lo siguiente 
        # return [a in (('llenar', 0), ('llenar', 1), ('vaciar', 0), ('vaciar', 1), ('pasar', 0, 1), ('pasar', 1, 0)) if 
        #             (a[0] == 'llenar' and estado[a[1]] < self.limites[a[1]]) or
        #             (a[0] == 'vaciar' and estado[a[1]] > 0) or
        #             (estado[a[1]] > 0 and estado[a[2]] < self.limites[a[2]])]
            

    def sucesor(self, estado, accion):
        e = list(estado)
        if accion[0] == 'llenar':
            e[accion[1]] = self.limites[accion[1]]
        elif accion[0] == 'vaciar':
            e[accion[1]] = 0
        elif accion[0] == 'pasar':
            vertido = min(self.limites[accion[2]] - e[accion[2]], e[accion[1]])
            e[accion[1]] -= vertido
            e[accion[2]] += vertido
        return tuple(e)



class PbDosBotesCosto(PbDosBotes):
    """
    El problema de los dos botes, donde lo que importa es la cantidad de agua que se utiliza

    """
    def costo_local(self, estado, accion):
        """
        En este caso el costo es 1 por movimiento, y si la acción es de llenar, 10 lts**2 (no lineal)

        """
        if accion[0] == 'llenar':
            return 1 + 10 * (self.limites[accion[1]] - estado[accion[1]]) ** 2
        return 1


def prueba_basico(problema):

    n = busquedas.busqueda_ancho(problema)
    print u"Utilizando búsqueda primero a lo ancho"
    print n
    print "\nY se tuvieron que checar ", n.nodos_visitados, " nodos."

    n = busquedas.busqueda_profundo(problema)
    print u"\n\nUtilizando búsqueda primero a lo profundo"
    print n
    print "\nY se tuvieron que checar ", n.nodos_visitados, " nodos."

    n = busquedas.busqueda_profundidad_iterativa(problema)
    print u"\n\nUtilizando búsqueda profundidad iterativa"
    print n
    print "\nY se tuvieron que checar ", n.nodos_visitados, " nodos."

    n = busquedas.busqueda_costo_uniforme(problema)
    print u"\n\nUtilizando búsqueda por costo uniforme"
    print n
    print "\nY se tuvieron que checar ", n.nodos_visitados, " nodos."


def problema_mas_complicado(clase_problema_dos_botes):

    # # En forma estructurada
    mejor = None
    costo = 0
    for maxA in range(3, 11):
        for maxB in range(2, maxA):
            for meta in range(1, maxA):
                n = busquedas.busqueda_costo_uniforme(clase_problema_dos_botes(maxA, maxB, meta))
                if n and n.costo > costo:
                    mejor, costo = (maxA, maxB, meta), n.costo

    # # En forma funcional
    # def costo_configuracion(config):
    #     n = busquedas.busqueda_ancho(PbDosBotes(*config))
    #     return 0 if not n else n.costo
    #
    # mejor = max([(maxA, maxB, meta) for maxA in range(3, 11) for maxB in range(2, maxA) for meta in range(1, maxA)],
    #             key=costo_configuracion)

    print "\n\n\n\n... el resutado es: ", mejor, " con un costo de ", costo, "\n"
    n = busquedas.busqueda_costo_uniforme(clase_problema_dos_botes(*mejor))
    print n


if __name__ == '__main__':

    print "Primero vamos a checar si funciona bien esto con un bote de 7, otro de 3 y una meta de 5"
    prueba_basico(PbDosBotes(7, 3, 5))

    print "\n" + "-" * 20 + '\n'
    print "Ahora checamos el problema con costo"
    prueba_basico(PbDosBotesCosto(7, 3, 5))

    print u"\n\n\n¿Cual será la combinación maxA, maxB, meta con maxA y maxB < 10 cuya solución optima requiera el mayor número de pasos?"
    problema_mas_complicado(PbDosBotes)
    
    print u"\n\n¿Y para el problema con costo?"
    problema_mas_complicado(PbDosBotesCosto)
    