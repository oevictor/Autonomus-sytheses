import unittest
from src.optimizers.genetic_algorithm import GeneticAlgorithm

class TestGeneticAlgorithm(unittest.TestCase):

    def setUp(self):
        self.ga = GeneticAlgorithm()

    def test_initialize_population(self):
        population = self.ga.initialize_population(size=10, gene_length=5)
        self.assertEqual(len(population), 10)
        self.assertTrue(all(len(individual) == 5 for individual in population))

    def test_evaluate_fitness(self):
        test_solution = [0, 1, 1, 0, 1]
        fitness = self.ga.evaluate_fitness(test_solution)
        self.assertIsInstance(fitness, (int, float))

    def test_select_parents(self):
        population = [[0, 1, 1, 0, 1], [1, 0, 0, 1, 0]]
        parents = self.ga.select_parents(population)
        self.assertEqual(len(parents), 2)

    def test_crossover(self):
        parent1 = [0, 1, 1, 0, 1]
        parent2 = [1, 0, 0, 1, 0]
        offspring = self.ga.crossover(parent1, parent2)
        self.assertEqual(len(offspring), 5)

    def test_mutate(self):
        individual = [0, 1, 1, 0, 1]
        mutated = self.ga.mutate(individual)
        self.assertNotEqual(individual, mutated)

    def test_run(self):
        best_solution = self.ga.run(generations=10, population_size=10)
        self.assertIsInstance(best_solution, list)

if __name__ == '__main__':
    unittest.main()