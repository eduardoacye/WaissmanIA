# -*- coding: utf-8 -*-
"""
hw01-2.py

Homework description
====================

2.- Disenia un Agente reactivo basado en modelo para este entorno y compara su desempenio con un agente 
aleatorio despues de 100 pasos de simulacion.

Valor de 25 puntos

"""

__author__ = 'eduardoacye'

import environment
import hw01_1
from random import choice

class RandomVacuum(environment.Agent):
    """
    An agent that performs valid actions randomly
    """
    def __init__(self, allowed_actions):
        self.actions = allowed_actions

    def determine_action(self, perception):
        location, status = perception
        x , y = location
        
        if y == 0:
            return choice(filter(lambda a: a != 'go up' , self.actions))
        elif y == 1:
            return choice(filter(lambda a: a != 'go down' , self.actions))
        else:
            return choice(self.actions)

class ReflexVacuumWithState(environment.Agent):
    """
    An agent that cleans just dirty rooms, doesn't stay on a clean room,
    keeps track of which rooms are clean and does nothing when has finished
    """
    def __init__(self, initial_state):
        location , rooms_status = initial_state
        x , y = location
        first_floor , second_floor = rooms_status
        self.memory = [[x,y],[list(first_floor),list(second_floor)]]
        self.last_resort = {1 : 'go up', 0 : 'go down'}

    def determine_action(self, perception):
        location, status = perception
        x , y = location

        # Update internal memory
        self.memory[0] = [x,y]
        self.memory[1][y][x] = status

        # Decide based on the internal memory
        if all(map(lambda i: i=='clean', self.memory[1][0]+self.memory[1][1])):
            return 'do nothing'
        elif status == 'dirty':
            return 'clean room'
        elif x == 0:
            if self.memory[1][y][x+1] == 'dirty':
                return 'go right'
            elif self.memory[1][(y+1)%2][x] == 'dirty':
                return self.last_resort[y]
            else:
                return 'go right'
        elif x == 2:
            if self.memory[1][y][x-1] == 'dirty':
                return 'go left'
            elif self.memory[1][(y+1)%2][x] == 'dirty':
                return self.last_resort[y]
            else:
                return 'go left'
        else:
            if self.memory[1][y][x-1] == 'dirty':
                return 'go left'
            elif self.memory[1][y][x+1] == 'dirty':
                return 'go right'
            elif self.memory[1][(y+1)%2][x] == 'dirty':
                return self.last_resort[y]
            else:
                return 'go left'

def test():
    initial_state = ((0,0),(('dirty','dirty','dirty'),('dirty','dirty','dirty')))
    initial_state2 = ((1,1),(('dirty','dirty','dirty'),('dirty','dirty','dirty')))
    initial_state3 = ((1,1),(('dirty','clean','dirty'),('clean','dirty','clean')))

    print "Testing the three by two room environment with a random vacuum"
    environment.simulate(hw01_1.ThreeByTwoRooms(),
                         RandomVacuum(('go right','go left','go up','go down','clean room','do nothing')),
                         initial_state3, 100)

    print "Testing the three by two room environment with a reflex vacuum with state"
    environment.simulate(hw01_1.ThreeByTwoRooms(),
                         ReflexVacuumWithState(initial_state),
                         initial_state3, 100)

if __name__ == '__main__':
    test()