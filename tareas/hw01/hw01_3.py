# -*- coding: utf-8 -*-
"""
hw01-3.py

Homework description
====================

3.- Al ejemplo original de los dos cuardos, modificalo de manera que el agente sabe en que cuarto se 
encuentra pero no sabe si está limpio o sucio. Diseña un agente racional para este problema, pruebalo
y comparalo con el agente aleatorio.

Valor de 25 puntos

"""


__author__ = 'eduardoacye'

import environment
import two_rooms

class TwoRoomsMod(two_rooms.TwoRooms):
    def sense(self, current_state):
        location, room_a, room_b = current_state
        return location

class VacuumMod(environment.Agent):
    def __init__(self):
        self.prev_action = 'move'
        self.clean_count = 0

    def determine_action(self, perception):
        location = perception

        if self.clean_count == 2:
            return 'do nothing'
        elif self.prev_action == 'move':
            self.clean_count += 1
            self.prev_action = 'clean'
            return 'clean room'
        elif location == 'A':
            self.prev_action = 'move'
            return 'go to B'
        else:
            self.prev_action = 'move'
            return 'go to A'
        
                
        

def test():
    print "Testing the two room modified environment with a random vacuum"
    environment.simulate(TwoRoomsMod(),
                         two_rooms.RandomVacuum(['go to A', 'go to B', 'clean room', 'do nothing']),
                         ('A', 'dirty', 'dirty'), 100)

    print "Testing the two room modified environment with the modified vacuum"
    environment.simulate(TwoRoomsMod(),
                         VacuumMod(),
                         ('A', 'dirty', 'dirty'), 100)

if __name__ == '__main__':
    test()
    