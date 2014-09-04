"""
two_rooms.py

translated from juliowaissman's source 'doscuartos.py'
"""

__author__ = 'eduardo.acye'

import environment
from random import choice

class TwoRooms(environment.Environment):
    """
    Class for a two room environment.
    
    The state is defined as (<location>, <room_a>, <room_b> where:
    <location> can be 'A' or 'B'
    <room_a> can be 'clean' or 'dirty'
    <room_b> can be 'clean' or 'dirty'
    
    The valid actions in every state are:
    'go to A', 'go to B', 'clean room' and 'do nothing'
    
    The perceptions are given by the tuple (<location>, <situation>) where:
    <location> can be 'A' or 'B'
    <situation> can be 'clean' or 'dirty'
    """
    
    def next_state(self, current_state, action):
        """
        Determine where the agent is supposed to go.
        """
        if not self.valid_action(current_state, action):
            raise ValueError("Not a valid action for the current state")
        
        location, room_a, room_b = current_state
            
        if action == 'go to A':
            return 'A', room_a, room_b
        elif action == 'go to B':
            return 'B', room_a, room_b
        elif action == 'do nothing':
            return current_state
        elif action == 'clean room' and location == 'A':
            return 'A', 'clean', room_b
        elif action == 'clean room' and location == 'B':
            return 'B', room_a, 'clean'
        else:
            raise ValueError("There is a problem with the current state")
                

    def sense(self, current_state):
        """
        What can be perceived from the <current_state>?
        """
        location, room_a, room_b = current_state
        if location == 'A':
            return location, room_a
        elif location == 'B':
            return location, room_b
        else:
            raise ValueError("There is a problem with the current state")

    def performance(self, current_state, action):
        """
        How much does the given <action> executed at the <current_state> cost in performance?
        """
        location, room_a, room_b = current_state
        if action == 'do nothing' and room_a == room_b == 'clean':
            return 0
        else:
            return -1

    def valid_action(self, state, action):
        """
        Determine if the <action> is valid on the given <state>
        """
        return action in ('go to A', 'go to B', 'clean room', 'do nothing')


class RandomVacuum(environment.Agent):
    """
    An agent that performs valid actions randomly
    """
    def __init__(self, allowed_actions):
        self.actions = allowed_actions

    def determine_action(self, perception):
        return choice(self.actions)

class ReflexVacuum(environment.Agent):
    """
    An agent that cleans just dirty rooms and doesn't stay on a clean room
    """
    def determine_action(self, perception):
        location, situation = perception
        if situation == 'dirty':
            return 'clean room'
        elif location == 'B':
            return 'go to A'
        elif location == 'A':
            return 'go to B'
        else:
            raise ValueError("There is a problem with the perception")

class ReflexVacuumWithState(environment.Agent):
    """
    An agent that cleans just dirty rooms, doesn't stay on a clean room,
    keeps track of which rooms are clean and does nothing when has finished
    """
    def __init__(self, initial_state):
        self.memory = initial_state
        self.place = {'A' : 1, 'B' : 2}

    def determine_action(self, perception):
        location, situation = perception
        
        # Update the internal memory
        self.memory[0] = location
        self.memory[self.place[location]] = situation
        
        # Decide based on the internal memory
        room_a = self.memory[1]
        room_b = self.memory[2]
        if room_a == room_b == 'clean':
            return 'do nothing'
        elif situation == 'dirty':
            return 'clean room'
        elif location == 'B':
            return 'go to A'
        elif location == 'A':
            return 'go to B'
        else:
            raise ValueError("There is a problem with the perception")

def test():
    print "Testing the two room environment with a random vacuum"
    environment.simulate(TwoRooms(),
                         RandomVacuum(['go to A', 'go to B', 'clean room', 'do nothing']),
                         ('A', 'dirty', 'dirty'), 100)
    
    print "Testing the two room environment with a reflex vacuum"
    environment.simulate(TwoRooms(),
                         ReflexVacuum(),
                         ('A', 'dirty', 'dirty'), 100)
    
    print "Testing the two room environment with a reflex vacuum with state"
    environment.simulate(TwoRooms(),
                         ReflexVacuumWithState(['A', 'dirty', 'dirty']),
                         ('A', 'dirty', 'dirty'), 100)
    
if __name__ == '__main__':
    test()
