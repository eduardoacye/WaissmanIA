# -*- coding: utf-8 -*-
"""
hw01-1.py

Homework description
====================

1.- Desarrolla un entorno similar al de los dos cuardos pero con tres cuartos en el primer piso, 
y tres cuartos en el segundo piso. Las acciones totales seran

A = {"irDerecha", "irIzquierda", "subir", "bajar", "limpiar" y "noOp"}

Las accion de "subir" solo es legal en el piso de abajo (cualquier cuarto), y la accion de "bajar"
solo es legal en el piso de arriba.

Las acciones de subir y bajar son mas costosas en termino de energia que ir a la derecha y a la 
izquierda, por lo que la funcion de desempenio debe de ser de tener limpios todos los cuartos,
con el menor numero de acciones posibles, y minimozando subir y bajar en relacion a ir a los lados.


Valor de 25 puntos

"""

__author__ = 'eduardoacye'

import environment

class ThreeByTwoRooms(environment.Environment):
    """
    Clas for a 3x2 rooms environment.
    
    The valid actions are:
    'go right', 'go left', 'go up', 'go down', 'clean room', 'do nothing'

    'go up' is only legal in the first floor and 'go down' is only legal in the
    second floor.

    The cost of performing 'go up' and 'go down' is bigger than performing 'go right'
    and 'go left'.

    The state is defined as (<location>, <rooms_status>) where:
    <location> is defined as two indexes (x,y) x in {0,1} and y in {0,1,2}
    <rooms_status> is defined as the status of each room:
        ((room_00,room_01,room_02),(room_10,room_11,room_12))
    where room_xy can be 'clean' or dirty

    The perceptions are given as (<location>,<room_status>) where:
    <location> is defined as two indexes (x,y) x in {0,1} and y in {0,1,2}
    <status> is defined as 'clean' or 'dirty'
    """

    def next_state(self, current_state, action):
        """
        Where is the agent supposed to go?
        """
        
        if not self.valid_action(current_state, action):
            raise ValueError("Not a valid action for the current state")
        
        location, rooms_status = current_state
        location = list(location)
        x , y = location
        rooms_status = [list(rooms_status[0]),list(rooms_status[1])]
        
        if action == 'go right':
            if x < 2:
                x += 1
            return (x,y), (tuple(rooms_status[0]), tuple(rooms_status[1]))
        elif action == 'go left':
            if x > 0:
                x -= 1
            return (x,y), (tuple(rooms_status[0]), tuple(rooms_status[1]))
        elif action == 'go up':
            y -= 1
            return (x,y), (tuple(rooms_status[0]), tuple(rooms_status[1]))
        elif action == 'go down':
            y += 1
            return (x,y), (tuple(rooms_status[0]), tuple(rooms_status[1]))
        elif action == 'clean room':
            rooms_status[y][x] = 'clean'
            return location, (tuple(rooms_status[0]),tuple(rooms_status[1]))
        elif action == 'do nothing':
            return current_state
        else:
            raise ValueError("There is a problem with the current state")

    def sense(self, current_state):
        """
        What can be perceived from the current state?
        """
        location, rooms_status = current_state
        x , y = location
        return location, rooms_status[y][x]
    
    def performance(self, current_state, action):
        """
        What is the cost in performance for executing an action on the current state?
        """
        location, rooms_status = current_state

        if action == 'do nothing' and all(map(lambda i: i=='clean',rooms_status[0]+rooms_status[1])):
            return 0
        elif action == 'go up' or action == 'go down':
            return -2
        else:
            return -1

    def valid_action(self, current_state, action):
        """
        Is the action that is about to be performed on the current state a valid one?
        """
        location, rooms_status = current_state
        
        if location[1] == 0:
            return action in ('go right','go left','go down','clean room','do nothing')
        elif location[1] == 1:
            return action in ('go right','go left','go up','clean room','do nothing')
        else:
            return action in ('go right','go left','go up','go down','clean room','do nothing')