import unittest
from src.optimizers.differential_evolution import DifferentialEvolution
from src.problems.sample_problem import evaluate_solution

class TestDifferentialEvolution(unittest.TestCase):

    def setUp(self):
        self.de = DifferentialEvolution()
        self.population_size = 10
        self.dimension = 2
        self.de.initialize_population(self.population_size, self.dimension)

    def test_initialize_population(self):
        self.assertEqual(len(self.de.population), self.population_size)
        for individual in self.de.population:
            self.assertEqual(len(individual), self.dimension)

    def test_evaluate_fitness(self):
        fitness_values = self.de.evaluate_fitness(evaluate_solution)
        self.assertEqual(len(fitness_values), self.population_size)

    def test_run(self):
        best_solution, best_fitness = self.de.run(evaluate_solution, iterations=100)
        self.assertIsNotNone(best_solution)
        self.assertIsInstance(best_fitness, float)

if __name__ == '__main__':
    unittest.main()