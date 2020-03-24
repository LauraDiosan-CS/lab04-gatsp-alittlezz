from random import randint, uniform

class GA:
    def __init__(self, params=None):
        self.__params = params
        self.__population = []

    @property
    def population(self):
        return self.__population

    def initialisation(self):
        for _ in range(0, self.__params['popSize']):
            c = self.__params['chromosome'](self.__params)
            c.initialize_labels()
            self.__population.append(c)

    def evaluation(self):
        for c in self.__population:
            c.fitness = self.__params['function'](c.route, self.__params['matrix'])
        self.__population = sorted(self.__population, key=lambda x: x.fitness)

    def bestChromosome(self):
        return self.__population[0]

    def worstChromosome(self):
        return self.__population[-1]

    def selection(self):
        pos1 = randint(0, self.__params['popSize'] - 1)
        pos2 = randint(0, self.__params['popSize'] - 1)
        return min(pos1, pos2)

    def oneGeneration(self):
        newPop = []
        parents = self.get_parents_random(self.__params['popSize'])
        for p1, p2 in parents:
            off = p1.crossover(p2)
            off.mutate()
            newPop.append(off)
        self.__population = newPop
        self.evaluation()

    def oneGenerationElitism(self):
        newPop = [self.bestChromosome()]
        parents = self.get_parents_random(self.__params['popSize'] - 1)
        for p1, p2 in parents:
            off = p1.crossover(p2)
            off.mutate()
            newPop.append(off)
        self.__population = newPop
        self.evaluation()

    def oneGenerationSteadyState(self):
        parents = self.get_parents_random(self.__params['popSize'])
        for p1, p2 in parents:
            off = p1.crossover(p2)
            off.mutate()
            off.fitness = self.__params['function'](off.route, self.__params['matrix'])
            worst = self.worstChromosome()
            if off.fitness < worst.fitness:
                self.__population[-1] = off
        self.evaluation()

    def get_parents_random(self, n):
        parents = []
        for _ in range(n):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            parents.append([p1, p2])
        return parents

    def get_parents_roulette(self, n):
        parents = []
        mx_fitness = self.bestChromosome().fitness + 1
        fitnesses = [mx_fitness - c.fitness for c in self.__population]
        total_fitness = sum(fitnesses)
        cr_sm = 0
        ratios = []
        for c in fitnesses:
            cr_sm += c
            ratios.append(cr_sm / total_fitness)
        ratios = list(reversed(ratios))
        for _ in range(n):
            p1 = self.__population[self.get_parent_binary_search(ratios, uniform(0, 1))]
            p2 = self.__population[self.get_parent_binary_search(ratios, uniform(0, 1))]
            parents.append([p1, p2])
        return parents

    def get_parent_binary_search(self, ratios, x):
        lf = 0
        rg = len(ratios) - 1
        sol = None
        while lf <= rg:
            md = (lf + rg) >> 1
            if ratios[md] >= x:
                sol = md
                lf = md + 1
            else:
                rg = md - 1
        return sol
