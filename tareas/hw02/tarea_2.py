#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tarea_2.py
------------

Tarea 2a: Dibujar un grafo utilizando métodos de optimización

Si bien estos métodos no son los que se utilizan en el dibujo de gráfos por computadora (son
algoritmos realmente muy complejos lo que se usan actualmente). Si da una idea de la utilidad de
los métodos de optimización en un problema divertido.

Obviamente el problema se encuentra muy simplificado para poder ser visto dentro de una práctica.

Para realizar este problema es ecesario contar con el módulo PIL (Python Image Library) instalada.
Si instalaste EPD o EPD free, no hay problema, PIL viene ya incluido. Si no, hay que instalarlo.

Para que funcione, este modulo debe de encontrarse en la misma carpeta que blocales.py (incluida en piazza)

"""

__author__ = 'eduardoacye'

import blocales
import random
import itertools
import math
import Image
import ImageDraw
import time


class problema_grafica_grafo(blocales.Problema):
    """
    Clase para un grafo simple no dirigido, únicamente para fines de graficación

    """

    def __init__(self, vertices, aristas, dimension_imagen=400):
        """
        Un grafo se define como un conjunto de vertices, en forma de lista (no conjunto, el orden es importante
        a la hora de graficar), y un conjunto (tambien en forma de lista) de pares ordenados de vertices, lo que
        forman las aristas.

        Igualmente es importante indicar la resolución de la imagen a mostrar (por default de 400x400 pixeles).

        @param vertices: Lista con el nombre de los vertices.
        @param aristas: Lista con el nombre de las aristas.
        @param dimension_imagen: Entero con la dimansion de la imagen en pixeles (cuadrada por facilidad).

        """
        self.vertices = vertices
        self.aristas = aristas
        self.dim = dimension_imagen

    def estado_aleatorio(self):
        """
        Devuelve un estado aleatorio.

        Un estado para este problema de define como s = [s(1), s(2), ..., s(2*len(vertices))] en donde:

        s(i) \in {10, 11, ..., 390} es la posición en x del nodo i/2 si i es par, o la posicion en y del
        nodo (i-1)/2 si i es non (osease las parejas (x,y)).

        @return: Una tupla con las posiciones (x1, y1, x2, y2, ...) de cada vertice en la imagen.

        """
        return tuple(random.randint(10, self.dim - 10) for _ in range(2 * len(self.vertices)))

    def vecino_aleatorio(self, estado):
        """
        Encuentra un vecino en forma aleatoria. En estea primera versión lo que hacemos es tomar un valor aleatorio,
        y sumarle o restarle uno al azar.

        Este es un vecino aleatorio muy malo. Por lo que deberás buscar como hacer un mejor vecino aleatorio y comparar
        las ventajas de hacer un mejor vecino en el algoritmo de temple simulado.

        @param estado: Una tupla con el estado.

        @return: Una tupla con un estado vecino al estado de entrada.

        """
        vecino = list(estado)
        i = random.randint(0, len(vecino) - 1)
        vecino[i] = max(10, min(self.dim - 10, vecino[i] + random.choice([-1, 1])))
        return vecino
#################################################################################################
#                          20 PUNTOS
#################################################################################################

####################################################################################################
# RESPUESTA  #
####################################################################################################
# En esta parte del problema opté por hacer dos versiones del temple simulado en espacios continuos
# una es con la distribución y calendarización de Cauchy y otra con la distribución y calendariza-
# ción de Boltzman.
#
# Las implementaciones se encuentran en el archivo blocales.py
#
# Aún no realizo pruebas objetivas de cómo es que estas variaciones mejoran la solución del problema
# sin embargo conceptualmente hablando considero que es mejor considerar un vecino de un determinado
# estado como alguna variante en las componentes de todos los puntos, de esta forma habría mas cambios
# en la imágen que se desea pintar (no solo un pequeño movimiento de una coordenada de un punto por
# cada iteración).
###################################################################################################

        # Por supuesto que esta no es la mejor manera de generar vecino para este problema.
        # Al ser muchos los pixeles, dentro del temple simulado, se podría generar los vecinos como
        # si fuera un problema continuo, y solamente se redondea el resultado obtenido (y se evita 
        # que un valor se salga de los valores máximos posibles, por supuesto).
        #
        # Prueba y ajusta el algoritmo de temple simulado para espacos continuos y redondea a 1 al
        # generar vecino aleatorio. Esto lo puedes agregar en este método, recibiendo no únicamente 
        # el estado actual, si no además información de la temperatura, por ejemplo, y algo más 
        # posiblemente. 
        #        
        # -- Escribe inmediatamenta arriba de este comentario tus respuestas a la pregunta, comenta el 
        #    código propuesto y agrega el tuyo.


    def costo(self, estado):
        """
        Encuentra el costo de un estado. En principio el costo de un estado es la cantidad de veces que dos
        aristas se cruzan cuando se dibujan. Esto hace que el dibujo se organice para tener el menor numero
        posible de cruces entre aristas.

        @param: Una tupla con un estado

        @return: Un número flotante con el costo del estado.

        """

        # Inicializa fáctores lineales para los criterios más importantes (default solo cuanta el criterio 1)
        K1 = 15.0
        K2 = 10.0
        K3 = 20.0
        K4 = 10.0

        # Genera un diccionario con el estado y la posición para facilidad
        estado_dic = self.estado2dic(estado)

        return (K1 * self.numero_de_cruces(estado_dic) + 
                K2 * self.separacion_vertices(estado_dic) + 
                K3 * self.angulo_aristas(estado_dic) + 
                K4 * self.criterio_propio(estado_dic))


        # Como podras ver en los resultados, este costo no hace figuras particularmente
        # bonitas, y esto es porque lo único que considera es el numero de cruces.
        #
        # Una manera de buscar mejores resultados es incluir en el costo el angulo entre dos aristas conectadas
        # al mismo vertice, dandole un mayor costo si el angulo es muy pequeño (positivo o negativo). Igualemtente
        # se puede penalizar el que dos nodos estén muy cercanos entre si en la gráfica
        #
        # Así, vamos a calcular el costo en tres partes, una es el numero de cruces (ya programada), otra
        # la distancia entre nodos (ya programada) y otro el angulo entre arista de cada nodo (para programar) y cada
        # uno de estos criterios hay que agregarlo a la función de costo con un peso.
        #


    def numero_de_cruces(self, estado_dic):
        """
        Devuelve el numero de veces que dos aristas se cruzan en el grafo si se grafica como dice estado

        @param estado_dic: Diccionario cuyas llaves son los vértices del grafo y cuyos valores es una
                           tupla con la posición (x, y) de ese vértice en el dibujo.

        @return: Un número.

        """
        total = 0

        # Por cada arista en relacion a las otras (todas las combinaciones de aristas)
        for (aristaA, aristaB) in itertools.combinations(self.aristas, 2):

            # Encuentra los valores de (x0A,y0A), (xFA, yFA) para los vartices de una arista
            # y los valores (x0B,y0B), (x0B, y0B) para los vertices de la otra arista
            (x0A, y0A), (xFA, yFA) = estado_dic[aristaA[0]], estado_dic[aristaA[1]]
            (x0B, y0B), (xFB, yFB) = estado_dic[aristaB[0]], estado_dic[aristaB[1]]

            # Utilizando la clasica formula para encontrar interseccion entre dos lineas
            # cuidando primero de asegurarse que las lineas no son paralelas (para evitar la
            # división por cero)
            den = (xFA - x0A) * (yFB - y0B) - (xFB - x0B) * (yFA - y0A) + 0.0
            if den == 0:
                continue

            # Y entonces sacamos el largo del cruce, normalizado por den. Esto significa que en 0
            # se encuentran en la primer arista y en 1 en la última. Si los puntos de cruce de ambas
            # lineas se encuentran en valores entre 0 y 1, significa que se cruzan
            puntoA = ((xFB - x0B) * (y0A - y0B) - (yFB - y0B) * (x0A - x0B)) / den
            puntoB = ((xFA - x0A) * (y0A - y0B) - (yFA - y0A) * (x0A - x0B)) / den

            if 0 < puntoA < 1 and 0 < puntoB < 1:
                total += 1

        return total

    def separacion_vertices(self, estado_dic, min_dist=50):
        """
        A partir de una posicion "estado" devuelve una penalización proporcional a cada par de vertices que se
        encuentren menos lejos que min_dist. Si la distancia entre vertices es menor a min_dist, entonces calcula una
        penalización proporcional a esta.

        @param estado_dic: Diccionario cuyas llaves son los vértices del grafo y cuyos valores es una
                           tupla con la posición (x, y) de ese vértice en el dibujo.
        @param min_dist: Mínima distancia aceptable en pixeles entre dos vértices en el dibujo.

        @return: Un número.

        """
        total = 0
        for (v1, v2) in itertools.combinations(self.vertices, 2):
            # Calcula la distancia entre dos vertices
            (x1, y1), (x2, y2) = estado_dic[v1], estado_dic[v2]
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

            # Penaliza la distancia si es menor a min_dist
            if dist < min_dist:
                total += (1.0 - (dist / min_dist))

        return total

    def angulo_aristas(self, estado_dic):
        """
        A partir de una posicion "estado", devuelve una penalizacion proporcional a cada angulo entre aristas
        menor a pi/6 rad (30 grados). Los angulos de pi/6 o mayores no llevan ninguna penalización, y la penalizacion
        crece conforme el angulo es menor.

        @param estado_dic: Diccionario cuyas llaves son los vértices del grafo y cuyos valores es una
                           tupla con la posición (x, y) de ese vértice en el dibujo.

        @return: Un número.

        """
        #################################################################################################
        #                          20 PUNTOS
        #################################################################################################
        # Agrega el método que considere el angulo entre aristas de cada vertice. Dale diferente peso a cada criterio
        # hasta lograr que el sistema realice gráficas "bonitas"
        #
        # ¿Que valores de diste a K1, K2 y K3 respectivamente?
        #
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO ------------------------------------------------------------------------
        #
        
        # Para calcular el ángulo entre dos rectas consideramos a vert1,vert2 y vert3, donde vert2 y vert3
        # inciden en vert1.
        # u = vert2 - vert1 o
        # ux, uy = vert2x-vert1x, vert2y-vert1y
        # v = vert3 - vert1 o
        # vx, vy = vert3x-vert1x, vert3y-vert1y
        # cos teta = abs((ux*vx + uy*vy)/(sqrt(ux*ux+uy*uy)*sqrt(vx*vx+vy*vy)))
        # teta = arccos(abs((ux*vx + uy*vy)/(sqrt(ux*ux+uy*uy)*sqrt(vx*vx+vy*vy))))
        #
        # Se penaliza a partir de pi/6
        # if teta < pi/6:
        #    total += pi/teta-6
        #
        # de esta manera si es exactamente pi/6 no se refleja en costo, pero entre mas pequeño sea el costo
        # aumenta.
        total = 0
        for v in self.vertices:
            incident_edges = filter(lambda e: v == e[0] or v == e[1], self.aristas)
            for two_edges in itertools.combinations(incident_edges, 2):
                # edge1 y edge2 son las tuplas de las aristas a las que les calcularemos el ángulo
                edge1, edge2 = two_edges

                # v1, v2, v3 son los vértices que conforman a edge1 y edge2
                v1 = v
                if edge1[0] == v:
                    v2 = edge1[1]
                else:
                    v2 = edge1[0]
                if edge2[0] == v:
                    v3 = edge2[1]
                else:
                    v3 = edge2[0]

                # coord_v1, coord_v2, coord_v3 son las coordenadas de cada uno de los vértices
                coord_v1 = estado_dic[v1]
                coord_v2 = estado_dic[v2]
                coord_v3 = estado_dic[v3]
                
                # vectAx y vectAy son las componentes del vector asociado a edge1
                vectAx, vectAy = coord_v2[0]-coord_v1[0] , coord_v2[1]-coord_v1[1]

                # vectBx y vectBy son las componentes del vector asociado a edge2
                vectBx, vectBy = coord_v3[0]-coord_v1[0] , coord_v3[1]-coord_v1[1]

                product = vectAx*vectBx + vectAy*vectBy
                denomin = math.sqrt(vectAx**2+vectAy**2) * math.sqrt(vectBx**2+vectBy**2)

                denomin += .01
                argum = product/denomin
                if argum > 1:
                    argum = 1
                if argum < -1:
                    argum = -1
                teta = math.acos(argum)

                if teta < math.pi/6:
                    total += math.pi/(teta+.01) -6
        
        return total

    def criterio_propio(self, estado_dic):
        """
        Implementa y comenta correctamente un criterio de costo que sea conveniente para que un grafo
        luzca bien.

        @param estado_dic: Diccionario cuyas llaves son los vértices del grafo y cuyos valores es una
                           tupla con la posición (x, y) de ese vértice en el dibujo.

        @return: Un número.

        """
        #################################################################################################
        #                          20 PUNTOS
        #################################################################################################
        # ¿Crees que hubiera sido bueno incluir otro criterio? ¿Cual?
        #
        # Desarrolla un criterio propio y ajusta su importancia en el costo total con K4 ¿Mejora el resultado? ¿En
        # que mejora el resultado final?
        #
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO ------------------------------------------------------------------------
        #

        #
        # Estaría suave incluir algo que involucre la simetría, estoy considerando revisar las distancias
        # de cada vértice con sus vecinos y penalizar entre mas diferentes sean, revisar quizá la varianza
        # posiblemente cambie esto...
        #
        # El método que voy a incluir es el de aumentar el costo entre mas difieran las distancias de un vértice
        # a sus vecinos.
        def dist(p1, p2):
            x = p1[0]-p2[0]
            y = p1[1]-p2[1]
            return math.sqrt(x**2+y**2)
        def variance(seq):
            n = len(seq)
            mean = sum(seq)/n
            return sum(map(lambda d: d**2, seq))/n - mean**2
        total = 0
        max_desv = 10
        for v in self.vertices:
            incident_edges = filter(lambda e: v == e[0] or v == e[1], self.aristas)
            distancias = map(lambda pts: dist(estado_dic[pts[0]], estado_dic[pts[1]]), incident_edges)
            dist_desv = math.sqrt(variance(distancias))
            if dist_desv > max_desv:
                total += dist_desv
        
        return total

    def estado2dic(self, estado):
        """
        Convierte el estado en forma de tupla a un estado en forma de diccionario

        @param: Una tupla con las posiciones (x1, y1, x2, y2, ...)

        @return: Un diccionario cuyas llaves son el nombre de cada arista y su valor es una tupla (x, y)

        """
        return {self.vertices[i]: (estado[2 * i], estado[2 * i + 1]) for i in range(len(self.vertices))}

    def dibuja_grafo(self, estado=None):
        """
        Dibuja el grafo utilizando PIL, donde estado es una
        lista de dimensión 2*len(vertices), donde cada valor es
        la posición en x y y respectivamente de cada vertice. dim es
        la dimensión de la figura en pixeles.

        Si no existe una posición, entonces se obtiene una en forma
        aleatoria.

        """
        if not estado:
            estado = self.estado_aleatorio()

        # Diccionario donde lugar[vertice] = (posX, posY)
        lugar = self.estado2dic(estado)

        # Abre una imagen y para dibujar en la imagen
        imagen = Image.new('RGB', (self.dim, self.dim), (255, 255, 255))  # Imagen en blanco
        dibujar = ImageDraw.ImageDraw(imagen)

        for (v1, v2) in self.aristas:
            dibujar.line((lugar[v1], lugar[v2]), fill=(255, 0, 0))

        for v in self.vertices:
            dibujar.text(lugar[v], v, (0, 0, 0))

        imagen.show()


def main():
    """
    La función principal

    """

    # Vamos a definir un grafo sencillo
    
    vertices_sencillo = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    aristas_sencillo = [('B', 'G'),
                        ('E', 'F'),
                        ('H', 'E'),
                        ('D', 'B'),
                        ('H', 'G'),
                        ('A', 'E'),
                        ('C', 'F'),
                        ('H', 'B'),
                        ('F', 'A'),
                        ('C', 'B'),
                        ('H', 'F')]
    
    """
    vertices_sencillo = ['A', 'B', 'C', 'D', 'E']
    aristas_sencillo = [('A','B'),('A','C'),('A','D'),('A','E'),
                        ('B','C'),('B','D'),('B','E'),
                        ('C','D'),('C','E'),
                        ('D','E')]
    """
    dimension = 400

    # Y vamos a hacer un dibujo del grafo sin decirle como hacer para ajustarlo.
    grafo_sencillo = problema_grafica_grafo(vertices_sencillo, aristas_sencillo, dimension)

    estado_aleatorio = grafo_sencillo.estado_aleatorio()
    grafo_sencillo.dibuja_grafo(estado_aleatorio)
    print "Costo del estado aleatorio: ", grafo_sencillo.costo(estado_aleatorio)

    # Ahora vamos a encontrar donde deben de estar los puntos
    tiempo_inicial = time.time()
    solucion = blocales.temple_simulado(grafo_sencillo, lambda i: 1000 * math.exp(-0.001 * i))
    #solucion = blocales.temple_simulado_cauchy(grafo_sencillo, .02, 10, dimension, lambda i: 1000 * math.exp(-0.0001*i))
    #solucion = blocales.temple_simulado_cauchy(grafo_sencillo, .0001, 10, dimension)
    #solucion = blocales.temple_simulado_boltzman(grafo_sencillo, 0.0001, 10, dimension)
    tiempo_final = time.time()
    grafo_sencillo.dibuja_grafo(solucion)
    print "\nUtilizando una calendarización exponencial con K = 1000 y delta = 0.0001"
    print "Costo de la solución encontrada: ", grafo_sencillo.costo(solucion)
    print "Tiempo de ejecución en segundos: ", tiempo_final - tiempo_inicial
    #################################################################################################
    #                          20 PUNTOS
    #################################################################################################
    # ¿Que valores para ajustar el temple simulado (T0 y K) son los que mejor resultado dan?
    #
    # ¿Que encuentras en los resultados?, ¿Cual es el criterio mas importante?
    #
    #
    # Probé varios valores de diferentes ordenes de magnitud con la temperatura inicial y el alpha del temple simulado
    # y noté que modificaba mas que nada lo que tardaba la simulación, dando resultados similares
    # al pintar el grafo, así que dejé la temperatura inicial como 1000 y el alpha le di .001. La ponderación de
    # los criterios para el costo es lo que tuvo mayor peso en la solución del problema (quizá los parámetros
    # que utilicé no sean los mas convenientes, pero quedé satisfecho con la manera en que se pintan las gráficas).
    #
    # En cuestión al tiempo de simulación, la variación del alpha afectaba mas que la temperatura inicial, con
    # T0 < 1000 casi no se notaba diferencia en la calidad del resultado.


    #################################################################################################
    #                          20 PUNTOS
    #################################################################################################
    # En general para obtener mejores resultados del temple simulado, es necesario utilizar una
    # función de calendarización acorde con el metodo en que se genera el vecino aleatorio.
    # Existen en la literatura varias combinaciones. Busca en la literatura diferentes métodos de
    # calendarización (al menos uno más diferente al exponencial) y ajusta los parámetros de cada
    # metodo para que obtenga la mejor solución posible en el menor tiempo posible.
    #
    # Escribe aqui tus comentarios y prueba otro metodo de claendarización para compararlo con el
    # exponencial.
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ------------------------------------------------------------------------
    # 
    # Implementé el temple con la calendarización para el método de Boltzman y el de Cauchy (están en blocales.py),
    # sin embargo, los resultados salen mejor y mas rápido con el temple y la calendarización que nos dió.
    # 
    # Los problemas que tuve al momento de probar diferentes parámetros para estos métodos es que tardan un chorro
    # en correr la simulación, para cada cambio de parámetro el temple y calendarización de Boltzman tardaba al
    # rededor de 220 segundos.
    #
    # El mas rápido fué el de Cauchy, con el cual obtuve resultados peores que con el temple discreto con la calendarización
    # exponencial. Pude probar mas variaciones en los parámetros, sin embargo no logré que mejorara la belleza de
    # las gráficas.




if __name__ == '__main__':
    main()