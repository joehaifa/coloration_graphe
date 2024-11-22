import random
from collections import deque
from Individual import Individual  # Ensure that the Individual class is correctly implemented

class GA:
    def __init__(self, n_individuals, n_genes, n_edges, main_graph):
        self.n_individuals = n_individuals
        self.n_genes = n_genes
        self.n_edges = n_edges
        self.main_graph = main_graph
        self.population = [Individual(n_genes=n_genes) for _ in range(n_individuals)]

    def add_individual(self, ind_new):
        self.population.append(ind_new)
        self.n_individuals += 1

    def find_best_individuals(self, percentage):
        best_individuals = []
        sorted_population = sorted([(self.fitness_of_individual(i), i) for i in range(self.n_individuals)], reverse=True)
        n_best = int(percentage * self.n_individuals)

        for _, idx in sorted_population[:n_best]:
            best_individuals.append(self.population[idx])
        return best_individuals

    def reproduce(self, population, new_ind):
        new_population = []
        n_individuals = len(population)

        for _ in range(new_ind):
            parent1 = self._get_random_int(0, n_individuals - 1)
            parent2 = (parent1 + self._get_random_int(1, n_individuals - 1)) % n_individuals
            son = population[parent1].reproduce(population[parent2])
            new_population.append(son)
        return new_population

    def mutate(self, population, new_ind):
        new_population = []

        for _ in range(new_ind):
            random_idx = self._get_random_int(0, len(population) - 1)
            new_individual = population[random_idx]
            new_individual.mutate()
            new_population.append(new_individual)
        return new_population

    def create_new_population(self, p_best, p_reproduce, p_mutations):
        # Calculate the number of individuals to select for each process
        total_ratio = p_best + p_reproduce + p_mutations
        n_best = int(self.n_individuals * (p_best / total_ratio))
        n_reproduce = int(self.n_individuals * (p_reproduce / total_ratio))
        n_mutations = self.n_individuals - n_best - n_reproduce  # Ensure population size remains consistent

        # Select the best individuals
        best_individuals = self.find_best_individuals(p_best / total_ratio)
        
        # Generate new individuals through reproduction and mutation
        reproduced_individuals = self.reproduce(best_individuals, n_reproduce)
        mutated_individuals = self.mutate(best_individuals, n_mutations)

        # Combine all new individuals to form the new population
        new_population = best_individuals + reproduced_individuals + mutated_individuals

        # If the new population is larger than needed, trim it to fit the target population size
        self.population = new_population[:self.n_individuals]
        
        # Recalculate fitness for reproduced and mutated individuals
        for i in range(n_best, self.n_individuals):
            self.fitness_of_individual(i)



    def fitness_of_individual(self, index):
        fit = self.population[index].get_fitness()

        if fit == 0:
            for i in range(self.n_genes):
                for neighbor in self.main_graph[i]:
                    if self.population[index].at(i) != self.population[index].at(neighbor):
                        fit += 1
            if fit == self.n_edges:
                fit += self.n_genes - self.population[index].get_num_of_colors()
            self.population[index].set_fitness(fit)
        return fit

    def print_population(self):
        for individual in self.population:
            individual.print_chromosome()
            print("Fitness:", individual.get_fitness())

    def correct_color(self, n_colors, percentage):
        target = int(self.n_individuals * (percentage / 100))
        return sum(1 for ind in self.population if ind.get_num_of_colors() == n_colors) >= target

    def main_loop(self, max_iterations, min_colors, p_best, p_cross, p_mutation,totaliteration):
        color_correct = False

        while totaliteration[0] < max_iterations and not color_correct:
            self.create_new_population(p_best, p_cross, p_mutation)
            color_correct = self.correct_color(min_colors, 100.0 - p_mutation)
            totaliteration[0] += 1

        # After completing the loop, save the best coloring
        self.save_best_coloring()

    def _get_random_int(self, start, end):
        return random.randint(start, end)

    def save_best_coloring(self, filename="best_solution.txt"):
        # Find the best individual
        best_individual = max(self.population, key=lambda ind: ind.get_fitness())
        
        # Extract the coloring (chromosome) from the best individual
        best_coloring = best_individual.chromosome
        num_colors_used = best_individual.get_num_of_colors()
        fitness = best_individual.get_fitness()

        # Save the coloring to a file in the specified format
        with open(filename, 'w') as file:
            file.write(f"Chromosome: {best_coloring}\n")
            file.write(f"Number of colors used: {num_colors_used}\n")
            file.write(f"Fitness: {fitness}\n")
        
        print(f"Best coloring saved to {filename}.")

