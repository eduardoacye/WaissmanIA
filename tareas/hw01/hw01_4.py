# -*- coding: utf-8 -*-
"""
hw01-4.py

Homework description
====================

4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo para que cuando el agente decida
aspirar, el 80% de las veces limpie pero el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
para este problema, pruebalo y comparalo con el agente aleatorio.

Valor de 25 puntos

"""

__author__ = 'eduardoacye'

from random import random
import environment
import two_rooms

class StochasticTwoRooms(two_rooms.TwoRooms):
    def next_state(self, current_state, action):
        if not self.valid_action(current_state, action):
            raise ValueError("Not a valid action for the current state")

        location, room_a, room_b = current_state

        will_clean = random()
        
        if action == 'go to A':
            return 'A', room_a, room_b
        elif action == 'go to B':
            return 'B', room_a, room_b
        elif action == 'do nothing':
            return current_state
        elif action == 'clean room' and location == 'A':
            if will_clean < .2:
                return current_state
            else:
                return 'A', 'clean', room_b
        elif action == 'clean room' and location == 'B':
            if will_clean < .2:
                return current_state
            else:
                return 'B', room_a, 'clean'
        else:
            raise ValueError("There is a problem with the current state")

        

def test():
    print "Testing the stochastic two room environment with a random vacuum"
    environment.simulate(StochasticTwoRooms(),
                         two_rooms.RandomVacuum(['go to A', 'go to B', 'clean room', 'do nothing']),
                         ('A', 'dirty', 'dirty'), 100)

    print "Testing the stochastic two room environment with a reflex vacuum with state"
    environment.simulate(StochasticTwoRooms(),
                         two_rooms.ReflexVacuumWithState(['A', 'dirty', 'dirty']),
                         ('A', 'dirty', 'dirty'), 100)

if __name__ == '__main__':
    test()