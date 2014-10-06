#!/usr/bin/env python
# -- coding: utf-8 --

"""
sudoku.py
------------

Este es el problema que deberan resolver para la tarea 2 sobre satisfaccion de restricciones.

En esta tarea no se pide desarrollar o modificar los algoritmos de satisfacción de restricciones
que se ofrecen, sino de utilizarlos para resolver un problema relativamente simple:

    Un solucionador de sudokus

Los Sudokus son unos juegos de origen Japones. El juego tiene un tablero de 9 x 9 casillas.
En cada casilla se debe asignar un número 1, 2, 3, 4, 5, 6, 7, 8 o 9.

La idea principal de juego es establecer los valores de los números en las casillas no
asignadas anteriormente si se considera que:

    a) Las casillas horizontales deben tener números diferentes entre si
    b) Las casillas verticales deben tener números diferentes entre si
    c) Las casillas que pertenecen al mismo grupo deben tener números diferentes entre si.

sea (r1, c1) el renglon y la columna de una casilla y (r2, c2) el renglon y la columna de otra casilla,
se dice que las casillas pertenecen al mismo grupo si y solo si r1/3 == r2/3 y c1/3 == c2/3
donde / es la división entera (por ejemplo 4/3 = 1 o 8/3 = 2).
Esto aplica si se considera 0 como la primer posición.

Para más información sobre sudokus, pueden googlearlo, buscarlos en wikipedia o comprar un librito
de sudokus de 8 pesos (cuidado, se puede perder mucho tiempo resolviendo sudokus).


Para revisar la tarea es necesario seguir las siguientes instrucciones:

Un Sudoku se inicializa como una lista de 81 valores donde los valores se encuentran de la manera siguiente:

    0   1   2 |  3   4   5 |  6   7   8
    9  10  11 | 12  13  14 | 15  16  17
   18  19  20 | 21  22  23 | 24  25  26
   -----------+------------+------------
   27  28  29 | 30  31  32 | 33  34  35
   36  37  38 | 39  ...

hasta llegar a la posición 81.


los valores que puede tener la lista son del 0 al 9. Si tiene un 0 entonces es que el valor es desconocido.


"""

__author__ = 'juliowaissman'


import csp

def row(i):
    return i/9

def col(i):
    return i%9

def same_row(i,j):
    return row(i) == row(j)

def same_col(i,j):
    return col(i) == col(j)

bloques = [0,0,0,1,1,1,2,2,2,
           0,0,0,1,1,1,2,2,2,
           0,0,0,1,1,1,2,2,2,
           3,3,3,4,4,4,5,5,5,
           3,3,3,4,4,4,5,5,5,
           3,3,3,4,4,4,5,5,5,
           6,6,6,7,7,7,8,8,8,
           6,6,6,7,7,7,8,8,8,
           6,6,6,7,7,7,8,8,8]

def same_blo(i,j):
    return bloques[i] == bloques[j]

def is_empty_list(lst):
    return len(lst) == 0 


class Sudoku(csp.ProblemaCSP):
    """
    Esta es la clase que tienen que desarrollar y comentar. Las variables están dadas
    desde 0 hasta 81 (un vector) tal como dice arriba. No modificar nada de lo escrito
    solamente agregar su código.

    """

    def __init__(self, pos_ini):
        """
        Inicializa el sudoku

        """
        csp.ProblemaCSP.__init__(self)

        self.dominio = {i: [val] if val > 0 else range(1, 10) for (i, val) in enumerate(pos_ini)}

        #=================================================================
        # 20 puntos: INSERTAR SU CÓDIGO AQUI (para vecinos)
        #=================================================================

        """
        Los vecinos será un diccionario que relaciona un índice en pos_ini con una lista de
        índices que corresponden al mismo renglón, a la misma columna o al mismo bloque.
        """
        self.vecinos = {}

        indices = range(0,81)
        for i in indices:
            self.vecinos[i] = filter(lambda j: i != j and (same_row(i,j) or same_col(i,j) or same_blo(i,j)),indices)

        # raise NotImplementedError("¡Es parte de la tarea completar este método!")

    def restriccion_binaria(self, (xi, vi), (xj, vj)):
        """
        El mero chuqui. Por favor comenta tu código correctamente

        """
        #===========================================================================
        # 20 puntos: INSERTAR SU CÓDIGO AQUI (restricciones entre variables vecinas)
        #===========================================================================

        """
        xi y xj van a ser índices, mientras que vi y vj valores en el dominio de las variables.
        
        Esta función debe regresar verdadero si no hay problema con que xi tenga valor vi y
        xj tenga valor vj
        """

        return not(xi in self.vecinos[xj] and vi == vj)

    def imprime_sdk(self, asignacion):
        """
        Imprime un sudoku en pantalla en forma más o menos graciosa. Esta función solo sirve para la tarea y
        para la revisión de la tarea. No modificarla por ningun motivo.

        """
        s = [asignacion[i] for i in range(81)]
        c = ''
        for i in range(9):
            c += ' '.join(str(s[9 * i + j]) + ("  |  " if j % 3 == 2 and j < 7 else "   ") for j in range(9))
            c += '\n-------------+----------------+---------------\n' if i % 3 == 2 and i < 7 else '\n'
        print c
    

if __name__ == "__main__":

    # Vamos a poner unos sudokus famosos pa empezar

    # Una forma de verificas si el código que escribiste es correcto
    # es verificando que la solución sea satisfactoria para estos dos
    # sudokus. (20 puntos)

    s1 = [0, 0, 3, 0, 2, 0, 6, 0, 0,
          9, 0, 0, 3, 0, 5, 0, 0, 1,
          0, 0, 1, 8, 0, 6, 4, 0, 0,
          0, 0, 8, 1, 0, 2, 9, 0, 0,
          7, 0, 0, 0, 0, 0, 0, 0, 8,
          0, 0, 6, 7, 0, 8, 2, 0, 0,
          0, 0, 2, 6, 0, 9, 5, 0, 0,
          8, 0, 0, 2, 0, 3, 0, 0, 9,
          0, 0, 5, 0, 1, 0, 3, 0, 0]

    print "="*30
    print "Solucionando un Sudoku dificil"
    sudoku1 = Sudoku(s1)
    sudoku1.imprime_sdk(s1)

    print "  Solucion con CSP bin:"
    sol1 = csp.solucion_CSP_bin(sudoku1)
    sudoku1.imprime_sdk(sol1)
    
    print "  Solucion con Min-Conf:"
    sol1min = csp.min_conflictos(sudoku1)
    sudoku1.imprime_sdk(sol1min)
    

    s2 = [4, 0, 0, 0, 0, 0, 8, 0, 5,
          0, 3, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 7, 0, 0, 0, 0, 0,
          0, 2, 0, 0, 0, 0, 0, 6, 0,
          0, 0, 0, 0, 8, 0, 4, 0, 0,
          0, 0, 0, 0, 1, 0, 0, 0, 0,
          0, 0, 0, 6, 0, 3, 0, 7, 0,
          5, 0, 0, 2, 0, 0, 0, 0, 0,
          1, 0, 4, 0, 0, 0, 0, 0, 0]

    print "="*30
    print "Y otro tambien dificil"
    sudoku2 = Sudoku(s2)
    sudoku2.imprime_sdk(s2)

    print "  Solucion con CSP bin:"
    sol2 = csp.solucion_CSP_bin(sudoku2)
    sudoku2.imprime_sdk(sol2)
    
    print "  Solucion con Min-Conf:"
    sol2min = csp.min_conflictos(sudoku2)
    sudoku2.imprime_sdk(sol2min)
    


    # 40 puntos:
    # Prueba la solucion de sudokus utilizando minimos conflictos
    # Escribe aqui cual funciona mejor y di porque crees que es mejor uno que otro para este problema
    # Inserta tanto texto en forma de comentario como consideres necesario.
    """
    Creo que todo se reduce a la comparacion de cantidad de variables y tamanio del dominio.

    Funciona mejor el metodo solucion_CSP_bin, el min_conflictos con el sudoku es bastante malo.

    Creo que el de min_conflictos no funciona bien porque es a final de cuentas una busqueda local,
    es decir, es factible caer en mínimos locales en donde cualquier cambio al valor de una variable
    resulte en una cantidad de conflictos mayor a la actual, pero que la asignación tenga una cantidad
    de conflictos mayor a cero.

    Si comparamos el problema de las n-reinas con el del sudoku podemos notar que la cantidad de soluciones
    con cero conflictos en el caso de las n-reinas es mayor a que el del sudoku. Por lo tanto en todo
    el espacio de posibles asignaciones, la cantidad de minimos globales de las n-reinas es mucho mayor al
    del sudoku.

    Nota: Si la cantidad de dígitos dados en un sudoku de 9x9 es al menos 17, entonces solo existe una
    solución que lo resuelve (solo un mínimo global). Lo leí en el internet pero no chequé ninguna
    demostracion o explicación intuitiva. Igual se me hace que está bien comparar este hecho con el que
    para tableros grandes del n-reinas, mas grandes la cantidad de soluciones.
    """
