"""
environment.py
--------------

translated from juliowaissman's source 'entornos.py'



"""

__author__ = 'eduardoacye'

class Environment(object):
    """
    Environment abstract class
    """

    def next_state(self, state, action):
        """
        Return the state that the environment is going to be
        if from <state> an agent performs an <action>.
        """
        pass

    def sense(self, state):
        """
        Return what can be perceived from the environment in
        the given <state>.
        """
        pass

    def performance(self, state, action):
        """
        Return the cost of executing the given <action> in the given <state>.
        """
        pass

    def valid_action(self, state, action):
        """
        Determine if the <action> is valid while being on the <state>.
        """
        return True

class Agent(object):
    """
    Agent abstract class
    """
    def determine_action(self, percept):
        """
        Given a <percept>, what action is the agent going to take.
        """
        pass

def print_simulation(env_type, agt_type, steps, performances, states, actions):
    """
    Print information about the simulation and show the recorded history.
    """
    print "\n\nSimulation of environment type " + env_type + "with the agent type " + agt_type + "\n"
    print 'Step'.center(10) + 'State'.center(40) + 'Action'.center(25) + 'Performance'.center(15)
    print '_' * (10 + 40 + 25 + 15)
    for i in range(steps):
        print (str(i).center(10) + str(states[i]).center(40) + str(actions[i]).center(25) +
                str(performances[i]).rjust(12))
    print '_' * (10 + 40 + 25 + 15) + '\n\n'

def simulate(environment, agent, initial_state, iterations = 10, verbose=True):
    """
    Run a simulation of the given <agent> acting upon the given <environment> in
    a generig way.
    """

    # Set the parameters initial values
    state = initial_state # The current state of the environment
    performance = 0 # The initial performance of the agent
    action = None # The initial action of the agent

    perception = None # What the agent can perceive?
    #ext_state = None # What is the next state of the environment?


    # Initialize the history of the simulation
    performance_history = [performance]
    state_history = [state]
    action_history = [None]

    # Iterations for the simulation
    for step in range(iterations):
        # What can the agent perceive from the environment
        perception = environment.sense(state)
        # What the agent is going to do in this situation
        action = agent.determine_action(perception)
        # Accumulate the cost of performing this action
        performance += environment.performance(state, action)

        # Get the state of the environment after performing the action
        state = environment.next_state(state, action)

        # Record the performance, state and action
        performance_history.append(performance)
        state_history.append(state)
        action_history.append(action)

    # Optional: display the history of the simulation
    if verbose:
        e_type = str(type(environment))
        a_type = str(type(agent))
        print_simulation(e_type, a_type, iterations,
                        performance_history, state_history, action_history)

    return state_history, action_history, performance_history
