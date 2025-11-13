import numpy as np
class DifferentialEvolution:
    def __init__(self, population_size=30, mutation_factor=0.8, crossover_rate=0.9,
                 generations=100, max_generations=None, **kwargs):
        """
        Accept both 'generations' and 'max_generations' for compatibility.
        """
        self.population_size = population_size
        self.mutation_factor = mutation_factor
        self.crossover_rate = crossover_rate
        # prefer explicit generations, fall back to max_generations if provided
        self.generations = int(generations if generations is not None else (max_generations or 100))
        self.max_generations = max_generations
        self.population = []

    def initialize_population(self, bounds):
        import numpy as np
        self.population = np.random.rand(self.population_size, len(bounds))
        for i in range(len(bounds)):
            self.population[:, i] = self.population[:, i] * (bounds[i][1] - bounds[i][0]) + bounds[i][0]

    def evaluate_fitness(self, fitness_function):
        return [fitness_function(individual) for individual in self.population]

    def mutate(self, target_idx):
        indices = list(range(self.population_size))
        indices.remove(target_idx)
        a, b, c = self.random_sample(indices, 3)
        mutant = self.population[a] + self.mutation_factor * (self.population[b] - self.population[c])
        return mutant

    def crossover(self, target, mutant):
        crossover_mask = np.random.rand(len(target)) < self.crossover_rate
        return np.where(crossover_mask, mutant, target)

    def run(self, fitness_fn, bounds, minimize=True):
        import numpy as np
        dim = len(bounds)
        pop = np.array([[np.random.uniform(lo, hi) for lo, hi in bounds]
                        for _ in range(self.population_size)])
        history = []
        def eval_pop(p):
            return np.array([fitness_fn(ind) for ind in p])
        fitness = eval_pop(pop)
        for g in range(self.generations):
            for i in range(self.population_size):
                idxs = [idx for idx in range(self.population_size) if idx != i]
                a, b, c = pop[np.random.choice(idxs, 3, replace=False)]
                mutant = np.clip(a + self.mutation_factor * (b - c),
                                 [lo for lo,_ in bounds],
                                 [hi for _,hi in bounds])
                trial = pop[i].copy()
                for j in range(dim):
                    if np.random.rand() < self.crossover_rate:
                        trial[j] = mutant[j]
                trial_fit = fitness_fn(trial)
                cond = trial_fit < fitness[i] if minimize else trial_fit > fitness[i]
                if cond:
                    pop[i] = trial
                    fitness[i] = trial_fit
            best_val = fitness.min() if minimize else fitness.max()
            history.append(best_val)
        best_idx = fitness.argmin() if minimize else fitness.argmax()
        return {
            'best_solution': pop[best_idx],
            'best_value': fitness[best_idx],
            'history': history
        }

    def random_sample(self, indices, count):
        import random
        return random.sample(indices, count)