import random
import numpy as np

def generateARandomPermutation(n):
    perm = [i for i in range(n)]
    pos1 = random.randint(0, n - 1)
    pos2 = random.randint(0, n - 1)
    perm[pos1], perm[pos2] = perm[pos2], perm[pos1]
    return perm

class NormalChromosome:
    def __init__(self, params=None):
        self.__params = params
        self.__repres = None
        self.__fitness = 0

    # Initialize labels for representation
    def initialize_labels(self):
        # Switch between initializations

        # Initialize a random permutation
        self.__repres = [i for i in range(self.__params['noNodes'])]
        random.shuffle(self.__repres)

        # Initialize the identity permutation and swap 2 elements
        #self.__repres = generateARandomPermutation(self.__params['noNodes'])

    @staticmethod
    def get_type():
        return 'Normal chrom'

    @property
    def fitness(self):
        return self.__fitness

    @property
    def route(self):
        return self.__repres

    @route.setter
    def route(self, route):
        self.__repres = route

    @fitness.setter
    def fitness(self, fit = 0.0):
        self.__fitness = fit

    #
    def crossover(self, other):
        self.normalize()
        other.normalize()

        left = random.randint(0, len(self.__repres) - 1)
        right = random.randint(0, len(self.__repres) - 1)

        left, right = min(left, right), max(left, right)

        used_genes = {}
        for x in self.__repres[left: right + 1]:
            used_genes[x] = 1
        route = [None for _ in range(self.__params['noNodes'])]
        i = left
        j = right + 1
        for _ in range(self.__params['noNodes']):
            if i >= left and i <= right:
                route[i] = self.__repres[i]
            else:
                if j == self.__params['noNodes']:
                    j = 0
                while other.route[j] in used_genes:
                    j += 1
                    if j == self.__params['noNodes']:
                        j = 0
                route[i] = other.route[j]
                j += 1

            i += 1
            if i == self.__params['noNodes']:
                i = 0

        c = NormalChromosome(self.__params)
        c.route = route

        return c

    def mutate(self):
        idx1 = random.randint(0, len(self.__repres) - 1)
        idx2 = random.randint(0, len(self.__repres) - 1)
        self.__repres[idx1], self.__repres[idx2] = self.__repres[idx2], self.__repres[idx1]

    def __str__(self):
        return 'Normal chromosome with fitness: ' + str(self.__fitness) + '\n'

    def __repr__(self):
        return 'Normal chromosome with fitness: ' + str(self.__fitness) + '\n'

    def normalize(self):
        idx0 = self.__repres.index(0)
        self.__repres = self.__repres[idx0: ] + self.__repres[: idx0]
