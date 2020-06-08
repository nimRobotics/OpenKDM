"""
Contains main class for calculating and visualizing the mechanism

@nimrobotics
"""

import numpy as np
import math

# ground for link a and p
link_a_pivot = (0,-10)
link_p_pivot = (0,0)


class My_mechanism(object):

    # The init function
    def __init__(self,a,b,p,q,omega):
        self.a = a                            # Rod a
        self.b = b                            # Rod b
        self.p = p                            # Rod p
        self.q = q                            # Rod q
        self.omega = omega                    # Angular speed of rod p in rad/s
        self.theta0 = 0                       # Initial angular position of rod a
        self.set0 = (0,-100)                  # for selecting one of the two solutions
        self.k=0                              # Initial time for animation
        self.conn_rod_angular_speed = []      # Classes for the graphs animation
        self.c_speed = []                     # storing piston speed
        self.c_time = []                      # storing the time intervals
        self.pos_old = 0                      # old position of the piston for c_dot calculation

    # Angular position of rod p as a function of time
    def theta(self,t):
        theta = self.theta0 + self.omega*t
        return theta

    # position of end point of rod p
    def rod_p_position(self,t):
        p_x = self.p*np.cos(self.theta(t))
        p_y = self.p*np.sin(self.theta(t))
        return p_x,p_y

    # position of end point of rod q
    def rod_q_position(self,t):
        px,py = self.rod_p_position(t)
        ax,ay = link_a_pivot
        c = ((self.p**2-px**2-py**2) - (self.a**2-ax**2-ay**2)) / (2*(ax-px))
        d = (py-ay)/(ax-px)
        D = (d*(px-c)+py)**2 - (1+d**2)*(py**2 + (px-c)**2 - self.p**2)
        if D<0:
            """
            any length combination resulting in complex i.e. mechanism breaks
            will be skipped
            """
            raise Exception('complex')
        D2 = D**0.5
        y0 = (d*(px-c)+py+D2)/(1+d**2)
        y1 = (d*(px-c)+py-D2)/(1+d**2)
        x0 = c+d*y0
        x1 = c+d*y1
        set1=(x0,y0)
        set2=(x1,y1)

        dist1 = math.hypot(set1[0] - self.set0[0], set1[1] - self.set0[1])
        dist2 = math.hypot(set2[0] - self.set0[0], set2[1] - self.set0[1])
        if dist1<dist2:
            self.set0=set1
            return set1[0],set1[1]
        else:
            self.set0=set2
            return set2[0],set2[1]

    # position of piston end (i.e. slider)
    def piston_position(self,t):
        q_x,q_y = self.rod_q_position(t)
        h0 = q_x+(self.b**2 - (q_y-link_a_pivot[1])**2)**0.5
        return h0

    # Piston speed
    def c_dot(self,t):
        c_x = self.piston_position(t)
        c_dot = abs(c_x-self.pos_old)/0.01  # dt = 0.01
        self.pos_old = c_x
        return c_dot

class My_mechanism_slider(object):

    # The init function
    def __init__(self,a,b,omega):
        self.a = a                            # Rod a
        self.b = b                            # Rod b
        self.omega = omega                    # Angular speed of rod a in rad/s
        self.theta0 = 0                       # Initial angular position of rod a
        self.set0 = (0,-100)                  # for selecting one of the two solutions
        self.k=0                              # Initial time for animation
        self.c_position = []                  # Piston position for animation
        self.c_speed = []                     # storing piston speed
        self.c_time = []                      # storing the time intervals
        self.pos_old = 0                      # old position of the piston for c_dot calculation

    # Angular position of rod p as a function of time
    def theta(self,t):
        theta = self.theta0 + self.omega*t
        return theta

    # position of end point of rod a
    def rod_a_position(self,t):
        return self.a*np.cos(self.theta(t)),self.a*np.sin(self.theta(t))

    # position of piston end (i.e. slider)
    def piston_position(self,t):
        a_x,a_y = self.rod_a_position(t)
        return a_x+(self.b**2 - (a_y-link_a_pivot[1])**2)**0.5

    # Piston speed
    def c_dot(self,t):
        c_x = self.piston_position(t)
        c_dot = abs(c_x-self.pos_old)/0.01  # dt = 0.01
        self.pos_old = c_x
        return c_dot
