
import math
import random
from collections import defaultdict
import operator

from agentClasses import Agent, Food


# Evolve a new set of agents via genetic algorithm
def evolve(params, past_agents, gen):

    elitism_num = int(math.floor(params['elitism'] * params['pop_size']))
    new_orgs = params['pop_size'] - elitism_num

    stats = defaultdict(int)
    for org in past_agents:
        if org.fitness > stats['BEST'] or stats['BEST'] == 0:
            stats['BEST'] = org.fitness

        if org.fitness < stats['WORST'] or stats['WORST'] == 0:
            stats['WORST'] = org.fitness

        stats['SUM'] += org.fitness
        stats['COUNT'] += 1

    stats['AVG'] = stats['SUM'] / stats['COUNT']


    # Keep the best performing agents
    orgs_sorted = sorted(past_agents, key=operator.attrgetter('fitness'), reverse=True)
    organisms_new = []
    for i in range(0, elitism_num):
        organisms_new.append(Agent(params, wih=orgs_sorted[i].wih, who=orgs_sorted[i].who, name=orgs_sorted[i].name))


    # Make children
    for w in range(0, new_orgs):

        canidates = range(0, elitism_num)
        math.random_index = random.sample(canidates, 2)
        org_1 = orgs_sorted[math.random_index[0]]
        org_2 = orgs_sorted[math.random_index[1]]

        # Genetic crossover
        crossover_weight = random.random()
        wih_new = (crossover_weight * org_1.wih) + ((1 - crossover_weight) * org_2.wih)
        who_new = (crossover_weight * org_1.who) + ((1 - crossover_weight) * org_2.who)

        # Mutate the network weights
        mutate = random.random()
        if mutate <= params['mutate']:

            mat_pick = random.uniform(0,1)

            if mat_pick == 0:
                index_row = random.uniform(0,params['hnodes']-1)
                wih_new[index_row] = wih_new[index_row] * random.uniform(0.9, 1.1)
                if wih_new[index_row] >  1: wih_new[index_row] = 1
                if wih_new[index_row] < -1: wih_new[index_row] = -1

            if mat_pick == 1:
                index_row = random.uniform(0,params['onodes']-1)
                index_col = random.uniform(0,params['hnodes']-1)
                who_new[index_row][index_col] = who_new[index_row][index_col] * random.uniform(0.9, 1.1)
                if who_new[index_row][index_col] >  1: who_new[index_row][index_col] = 1
                if who_new[index_row][index_col] < -1: who_new[index_row][index_col] = -1

        organisms_new.append(Agent(params, wih=wih_new, who=who_new, name='gen['+str(gen)+']-org['+str(w)+']'))

    return organisms_new, stats
