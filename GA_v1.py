# edited from Eduardo I. 

import random
import numpy as np
import matplotlib.pyplot as plt

class Microbial():
    def __init__(self, fitnessFunction, popsize, genesize, recombProb, mutatProb):
        self.fitnessFunction = fitnessFunction
        self.popsize = popsize
        self.genesize = genesize
        self.recombProb = recombProb
        self.mutatProb = mutatProb
        self.pop = np.random.rand(popsize,genesize)*2 - 1
        self.avgHistory = []
        self.bestHistory = []

        
    def fitStats(self):
        bestfit = 0
        bestind = -1
        avgfit = 0
        for i in self.pop:
            fit = self.fitnessFunction(i)
            avgfit += fit
            if (fit > bestfit):
                bestfit = fit
                bestind = i
        return avgfit/self.popsize, bestfit, bestind

    def run(self,tournaments):

        # Evolutionary loop
        for i in range(tournaments):

            # Report statistics every generation
            if (i%self.popsize==0):
                print(i/self.popsize)
                af, bf, bi = self.fitStats()
                self.avgHistory.append(af)
                self.bestHistory.append(bf)

            # Step 1: Pick 2 individuals
            a = random.randint(0,self.popsize-1)
            b = random.randint(0,self.popsize-1)
            while (a==b):   # Make sure they are two different individuals
                b = random.randint(0,self.popsize-1)

            # Step 2: Compare their fitness
            if (self.fitnessFunction(self.pop[a]) > self.fitnessFunction(self.pop[b])):
                winner = a
                loser = b
            else:
                winner = b
                loser = a

            # Step 3: Transfect loser with winner
            for l in range(self.genesize):
                if (random.random() < self.recombProb):
                    self.pop[loser][l] = self.pop[winner][l]

            # Step 4: Mutate loser and Make sure new organism stays within bounds
##            for l in range(self.genesize):
##                self.pop[loser][l] += random.gauss(0.0,self.mutatProb)
##                if self.pop[loser][l] > 1.0:
##                    self.pop[loser][l] = 1.0
##                if self.pop[loser][l] < -1.0:
##                    self.pop[loser][l] = -1.0
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


