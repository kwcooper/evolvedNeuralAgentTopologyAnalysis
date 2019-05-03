

import random
import math
import numpy as np

# TODO:
#   add easy switching param between sigmoid and tahn
class Agent():
    def __init__(self, settings, wih=None, who=None, name=None):

        self.x = random.uniform(settings['x_min'], settings['x_max'])  # position (x)
        self.y = random.uniform(settings['y_min'], settings['y_max'])  # position (y)

        self.r = random.uniform(0,360)                 # orientation   [0, 360]
        self.v = random.uniform(0,settings['v_max'])   # velocity      [0, v_max]
        self.dv = random.uniform(-settings['dv_max'], settings['dv_max'])   # dv

        self.d_food = 100   # distance to nearest food
        self.r_food = 0     # orientation to nearest food
        self.fitness = 0    # fitness (food count)

        self.wih = wih
        self.who = who

        self.name = name


    # Define the network
    def think(self):
        af = lambda x: np.tanh(x)               
        # af = lambda x: self.sigmoid(x)
        h1 = af(np.dot(self.wih, self.r_food))  
        out = af(np.dot(self.who, h1))          

        self.nn_dv = float(out[0])   # [-1, 1]  (accelerate=1, deaccelerate=-1)
        self.nn_dr = float(out[1])   # [-1, 1]  (left=1, right=-1)

    # To change the heading
    def update_r(self, settings):
        self.r += self.nn_dr * settings['dr_max'] * settings['dt']
        self.r = self.r % 360


    # To change the velocity
    def update_vel(self, settings):
        self.v += self.nn_dv * settings['dv_max'] * settings['dt']
        if self.v < 0: self.v = 0
        if self.v > settings['v_max']: self.v = settings['v_max']


    # To change the position
    def update_pos(self, settings):
        dx = self.v * math.cos(math.radians(self.r)) * settings['dt']
        dy = self.v * math.sin(math.radians(self.r)) * settings['dt']
        self.x += dx
        self.y += dy

    # define the sigmoid activation function
    def sigmoid(self, x, derivative=False):
        sigm = 1. / (1. + np.exp(-x))
        if derivative:
            return sigm * (1. - sigm)
        return sigm


# Who's hungry?
class Food():
    def __init__(self, settings):
        self.x = random.uniform(settings['x_min'], settings['x_max'])
        self.y = random.uniform(settings['y_min'], settings['y_max'])
        self.energy = 1


    def respawn(self,settings):        
        self.x = random.uniform(settings['x_min'], settings['x_max'])
        self.y = random.uniform(settings['y_min'], settings['y_max'])
        self.energy = 1
