import numpy as np
class GeneticAlgorithm:

    def __init__(self, population_size, mutation_rate, crossover_rate, generations):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.population = []

    def initialize_population(self, bounds):
        import numpy as np
        self.population = np.random.uniform(bounds[0], bounds[1], (self.population_size, len(bounds[0])))

    def evaluate_fitness(self, fitness_function):
        return [fitness_function(individual) for individual in self.population]

    def select_parents(self, fitness):
        import numpy as np
        probabilities = fitness / np.sum(fitness)
        parents_indices = np.random.choice(range(self.population_size), size=2, p=probabilities)
        return self.population[parents_indices]

    def crossover(self, parent1, parent2):
        import numpy as np
        # ensure we can handle sequences of any small length
        n = len(parent1)
        if n < 2:
            # nothing to crossover, return copies
            try:
                return parent1.copy(), parent2.copy()
            except Exception:
                return parent1, parent2

        # choose split point in [1, n-1] safely by using high=n
        point = np.random.randint(1, n)
        child1 = np.concatenate([parent1[:point], parent2[point:]])
        child2 = np.concatenate([parent2[:point], parent1[point:]])
        return child1, child2

    def mutate(self, individual):
        for i in range(len(individual)):
            if np.random.rand() < self.mutation_rate:
                individual[i] += np.random.normal()
        return individual

    def run(self, fitness_fn, bounds, minimize=True):
        import numpy as np
        dim = len(bounds)
        pop = np.array([np.array([np.random.uniform(lo, hi) for lo, hi in bounds])
                        for _ in range(self.population_size)])
        history = []
        def eval_pop(p):
            vals = [fitness_fn(ind) for ind in p]
            return np.array(vals)
        for g in range(self.generations):
            fitness = eval_pop(pop)
            if minimize:
                best_idx = np.argmin(fitness)
                best_val = fitness[best_idx]
            else:
                best_idx = np.argmax(fitness)
                best_val = fitness[best_idx]
            history.append(best_val)
            parents = pop[np.random.choice(len(pop), 2, replace=False)]
            child1, child2 = self.crossover(parents[0], parents[1])
            def mutate(child):
                for i in range(dim):
                    if np.random.rand() < self.mutation_rate:
                        lo, hi = bounds[i]
                        child[i] = np.random.uniform(lo, hi)
                return child
            child1 = mutate(child1)
            child2 = mutate(child2)
            pop[np.random.choice(len(pop))] = child1
            pop[np.random.choice(len(pop))] = child2
        fitness = eval_pop(pop)
        if minimize:
            best_idx = np.argmin(fitness)
            best_val = fitness[best_idx]
        else:
            best_idx = np.argmax(fitness)
            best_val = fitness[best_idx]
        return {
            'best_solution': pop[best_idx],
            'best_value': best_val,
            'history': history
        }