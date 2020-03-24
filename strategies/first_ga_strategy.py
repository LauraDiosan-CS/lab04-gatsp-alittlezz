from GA import GA
from normal_chromosome import NormalChromosome
from professor_chromosome import ProfessorChromosome
from strategies.strategy import Strategy
import numpy as np
import matplotlib.pyplot as plt


class NormalGA(Strategy):
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.name = 'Normal GA'

    def solve(self, file_name, params=None, origin=None, destination=None):
        distance_matrix, origin, destination = self.read_distance_matrix(file_name)
        n = len(distance_matrix)
        param = {
            'noNodes': n,
            'matrix': distance_matrix,
            'popSize': params['popSize'],
            'chromosome': NormalChromosome,
            'function': self.get_real_distance,
            'noGen': params['noGen']
        }

        ga = GA(param)
        ga.initialisation()
        ga.evaluation()
        bestFitnesses = []
        averageFitnesses = []
        for i in range(param['noGen']):
            bc = ga.bestChromosome()
            bestFitnesses.append(bc.fitness)
            averageFitnesses.append(sum(c.fitness for c in ga.population) / len(ga.population))
            print("At generation", i + 1, "best chromosome has fitness", bc.fitness)
            ga.oneGenerationSteadyState()

        X = np.array([i for i in range(param['noGen'])])
        Y = np.array(averageFitnesses)
        Z = np.array(bestFitnesses)
        plt.scatter(X, Y)
        plt.scatter(X, Z)
        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.show()

        return bc.fitness, bc.route
