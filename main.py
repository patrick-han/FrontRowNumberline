import matplotlib.pyplot as pyplot
import math
import numpy as np


def phi_dot(y): # User modifies this function for the potential field force
    # phi = 2 * cos(y)
    return -2 * math.sin(y)


class Simulator:
    def __init__(self, state_in, phi_dot_in):
        self.state = state_in
        self.m = 1
        self.phi_dot = phi_dot_in

        # Crash constants -- dunno what these should be
        self.p_c = 0.5
        self.v_max = 3.0

    """
    Args:
    u - input force per timestep on range [-1, 1]

    Returns:
    nothing
    """
    def update_state(self, u):
        current_y = self.state[0]
        current_v = self.state[1]

        # Calculate new y
        sigma_d = 0.1 * current_v
        d = np.random.normal(loc = 0.0, scale = sigma_d)
        new_y = current_y + current_v + d

        # Calculate new v, with potential crash
        # Calculate probability and clamp to [0, 1)
        prob = np.clip((np.abs(current_v) - self.v_max) * self.p_c / self.v_max, 0.0, 1.0)
        # print("Probability of crashing: {} (pre-clip)".format((np.abs(current_v) - self.v_max) * self.p_c / self.v_max))
        # print("Probability of crashing: {}".format(prob))
        if np.random.rand() < prob:
            # Crashed!
            new_v = 0.0
            print("Crashed!")
        else:
            f_net = u - self.phi_dot(current_y)
            new_v = current_v + (1 / self.m) * f_net

        # Update state values
        self.state[0] = new_y
        self.state[1] = new_v

    """
    Args:
    nothing

    Returns:
    Calculated observaton from the noisy "sensor"
    """
    def calculate_observation(self):
        current_y = self.state[0]
        current_v = self.state[1]
        sigma_n = 0.5 * current_v
        if sigma_n == 0:
            n = 0
        else:
            n = np.random.normal(loc = 0.0, scale = sigma_n)
        return current_y + n

    """
    Args:
    nothing

    Returns:
    Current state vector
    """
    def get_state(self):
        return self.state

# current velocity at time t
v = 0.0

# current position at time t
y = 0.0

timestep = 0

init_state = [y, v]
my_sim = Simulator(init_state, phi_dot)
while(1):
    my_sim.update_state(0.1)
    print("Time: {}  |  Current state [y, v]: {}  |  Observation: {}".format(timestep, my_sim.get_state(), my_sim.calculate_observation()))
    input()
    timestep += 1