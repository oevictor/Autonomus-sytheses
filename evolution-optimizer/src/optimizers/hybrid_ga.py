import numpy as np

class HybridGA:
    """
    Genetic Algorithm using a surrogate model (e.g. Random Forest) as fitness.
    Allows variable-specific mutation probabilities derived from feature importance.
    """
    def __init__(
        self,
        population_size=40,
        generations=120,
        base_mutation_rate=0.05,
        crossover_rate=0.7,
        elitism=2,
        variable_mutation_weights=None
    ):
        self.population_size = population_size
        self.generations = generations
        self.base_mutation_rate = base_mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism = elitism
        self.variable_mutation_weights = variable_mutation_weights

    def _init_population(self, bounds):
        pop = []
        for _ in range(self.population_size):
            individual = np.array([np.random.uniform(lo, hi) for lo, hi in bounds])
            pop.append(individual)
        return np.array(pop)

    def _evaluate(self, pop, model):
        return model.predict(pop)

    def _tournament(self, pop, fitness, k=3):
        idxs = np.random.choice(len(pop), k, replace=False)
        best = idxs[np.argmax(fitness[idxs])]
        return pop[best]

    def _crossover(self, p1, p2):
        if np.random.rand() > self.crossover_rate:
            return p1.copy(), p2.copy()
        point = np.random.randint(1, len(p1))
        c1 = np.concatenate([p1[:point], p2[point:]])
        c2 = np.concatenate([p2[:point], p1[point:]])
        return c1, c2

    def _mutate(self, individual, bounds):
        dim = len(individual)
        # Normalize variable weights
        if self.variable_mutation_weights is not None:
            w = np.array(self.variable_mutation_weights, dtype=float)
            if w.sum() > 0:
                w = w / w.sum()
            else:
                w = np.ones(dim) / dim
        else:
            w = np.ones(dim) / dim

        for i in range(dim):
            # Importance-driven probability scaling
            prob = self.base_mutation_rate * (1.0 + 2.5 * w[i])
            if np.random.rand() < prob:
                lo, hi = bounds[i]
                # Local or global jump mix
                if np.random.rand() < 0.7:
                    span = hi - lo
                    step = np.random.normal(0, 0.15 * span)
                    individual[i] = np.clip(individual[i] + step, lo, hi)
                else:
                    individual[i] = np.random.uniform(lo, hi)
        return individual

    def run(self, model, bounds):
        pop = self._init_population(bounds)
        history = []
        for g in range(self.generations):
            fitness = self._evaluate(pop, model)
            best_idx = np.argmax(fitness)
            history.append(fitness[best_idx])
            # Sort by fitness
            order = np.argsort(fitness)[::-1]
            pop = pop[order]
            fitness = fitness[order]

            new_pop = [pop[i].copy() for i in range(self.elitism)]  # elitism

            while len(new_pop) < self.population_size:
                p1 = self._tournament(pop, fitness)
                p2 = self._tournament(pop, fitness)
                c1, c2 = self._crossover(p1, p2)
                c1 = self._mutate(c1, bounds)
                if len(new_pop) < self.population_size:
                    new_pop.append(c1)
                if len(new_pop) < self.population_size:
                    c2 = self._mutate(c2, bounds)
                    new_pop.append(c2)

            pop = np.array(new_pop)

        fitness = self._evaluate(pop, model)
        best_idx = np.argmax(fitness)
        return {
            "best_solution": pop[best_idx],
            "best_fitness": fitness[best_idx],
            "history": history
        }