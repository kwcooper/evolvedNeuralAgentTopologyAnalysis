
#  A huge thank you to Eduardo I, Nathan Rooy for much of the GA code


from __future__ import division, print_function
import math
import random
from collections import defaultdict
import operator

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.lines as lines
import numpy as np

from plottingFuncts import plot_food, plot_organism2, plot_frame
from agentClasses import Agent, Food
from GA import evolve


import time
import pickle



# Parameters
params = {}

# Evolution params
params['pop_size'] = 15       # number of agents
params['food_num'] = 115      # number of food particles
params['respawn'] = True      # respawn food?
params['gens'] = 2            # number of generations
params['elitism'] = 0.20      # elitism (selection bias)
params['mutate'] = 0.10       # mutation rate

# Network
params['inodes'] = 1          # number of input nodes
params['hnodes'] = 5          # number of hidden nodes
params['onodes'] = 2          # number of output nodes

# Sim params
params['gen_time'] = 50       # generation length (seconds)
params['dt'] = 0.04           # time step (dt)
params['dr_max'] = 720        # max rotational speed (degrees per second)
params['v_max'] = 0.5         # max velocity (units per second)
params['dv_max'] =  0.25      # max acceleration  (units per second^2)
params['x_min'] = -2.0        # western border
params['x_max'] =  2.0        # eastern border
params['y_min'] = -2.0        # southern border
params['y_max'] =  2.0        # northern border

params['plot'] = True        # plot final generation? (SLOW!)



def dist(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)


def calc_heading(agent, food):
    d_x = food.x - agent.x
    d_y = food.y - agent.y
    theta_d = math.degrees(math.atan2(d_y, d_x)) - agent.r
    if abs(theta_d) > 180: theta_d += 360
    return theta_d / 180


def simulate(params, agents, foods, gen):

    total_time_steps = int(params['gen_time'] / params['dt'])

    # iterate over timesteps
    for t_step in range(0, total_time_steps, 1):
        
        if params['plot']==True and gen==params['gens']-1:
            plot_frame(params, agents, foods, gen, t_step)

        # compute simulation step
        food_del = []
        for food_i in range(len(foods)):
            food = foods[food_i]
            for agent in agents:
                food_org_dist = dist(agent.x, agent.y, food.x, food.y)

                # Check if we're eating today
                if food_org_dist <= 0.075:
                    agent.fitness += food.energy
                    if  params['respawn'] == True:
                        food.respawn(params)
                    else:
                        food_del.append(food_i)
                        
                # reset agents head and dir        
                agent.d_food = 100
                agent.r_food = 0

        # eat the foods
        if params['respawn'] != True:
            if 0:
                print('lenfd', len(food_del))
                print('before:', len(foods))
            for idx in sorted(food_del, reverse=True):
                del foods[idx]
            if 0: print('after:', len(foods))
        
        # Compute dist to food
        for food in foods:
            for agent in agents:

                food_org_dist = dist(agent.x, agent.y, food.x, food.y)

                if food_org_dist < agent.d_food:
                    agent.d_food = food_org_dist
                    agent.r_food = calc_heading(agent, food)

        # Run the neural network
        for agent in agents:
            agent.think()

        # Update agent with net output
        for agent in agents:
            agent.update_r(params)
            agent.update_vel(params)
            agent.update_pos(params)

    return agents



def run(params):

    # Create food and agents
    foods = []
    for i in range(0,params['food_num']):
        foods.append(Food(params))

    agents = []
    for i in range(0,params['pop_size']):
        wih_init = np.random.uniform(-1, 1, (params['hnodes'], params['inodes']))     # mlp weights (input -> hidden)
        who_init = np.random.uniform(-1, 1, (params['onodes'], params['hnodes']))     # mlp weights (hidden -> output)

        agents.append(Agent(params, wih_init, who_init, name='gen[x]-agent['+str(i)+']'))

    # Iterate over generations
    fitnessList = []
    nets = {}
    for gen in range(0, params['gens']):

        agents = simulate(params, agents, foods, gen)

        # Grab the networks
        nets[gen] = {}
        c = 0
        for agent in agents:
            nets[gen][c] = {}
            nets[gen][c]['wih'] = agent.wih
            nets[gen][c]['who'] = agent.who
            nets[gen][c]['fit'] = agent.fitness
            #nets[gen][''] =

            c += 1

        # Evolve the organisms
        agents, stats = evolve(params, agents, gen)
        # agents, stats = Microbial(fitnessFunction, params['pop_size'], 2, params['mutate'] , params['elitism'])
        print('> Generation:',gen+1,'/', params['gens'], ' | Top:',stats['BEST'],'Mean:',stats['AVG'],'Worst:',stats['WORST'])
        
    # save our hard work!
    netsave = {}
    netsave['params'] = params
    netsave['nets'] = nets
    print('Saving nets...')
    fnamep = 'nets/nets_' + str(int(time.time())) + '.pickle'
    with open(fnamep, 'wb') as handle:
        pickle.dump(netsave, handle, protocol=pickle.HIGHEST_PROTOCOL)

    pass


if __name__ == "__main__":
    run(params)
    print('fin')

