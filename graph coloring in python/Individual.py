import random
from collections import deque
import os
import random

class Individual:

    def __init__(self, n_genes=None, chromosome=None):
        self.chromosome = []
        self.n_genes = n_genes if n_genes is not None else 0
        self.n_colors_used = 0
        self.fitness = 0

        if n_genes is not None and chromosome is None:
            self.chromosome = [self._get_random_int(0, n_genes) for _ in range(n_genes)]
            self.chromosome[0] = 0  # Start with first color at the beginning
            color = 0
            for i in range(1, n_genes):
                if self.chromosome[i] == 0:
                    self.chromosome[i] = color
                else:
                    color += 1
                    self.chromosome[i] = color
        elif chromosome is not None:
            self.chromosome = chromosome[:]
            self.n_genes = len(chromosome)


    def get_num_of_colors(self):
        """
        Calculates and returns the number of unique colors used in the chromosome.

        :return: The number of distinct colors.
        """
        return len(set(self.chromosome))


    def print_chromosome(self):
        """
        Prints the chromosome along with the number of colors used.
        """
        print("Chromosome:", self.chromosome, "Number of colors used:", self.get_num_of_colors())


    def at(self, i):
        """
        Returns the color at a specific index in the chromosome.

        :param i: The index of the gene.
        :return: The color value at the given index.
        """
        return self.chromosome[i]


    def set_fitness(self, fitness):
        """
        Sets the fitness value for the individual.

        :param fitness: The fitness value to assign.
        """
        self.fitness = fitness


    def get_fitness(self):
        """
        Retrieves the current fitness value of the individual.

        :return: The fitness value.
        """
        return self.fitness


    def mutate(self):
        """
        Mutates the individual's chromosome by swapping random genes to introduce variation.
        """
        self.fitness = 0
        max_iterations = self.n_genes // 2
        random_a = self._get_random_int(1, max_iterations)

        for i in range(random_a):
            random_b = self._get_random_int(0, self.n_genes - 1)
            swap_idx = (random_b + i + random_a) % self.n_genes
            self.chromosome[random_b], self.chromosome[swap_idx] = self.chromosome[swap_idx], self.chromosome[random_b]


    def reproduce(self, parent2):
        """
        Creates a new individual by combining parts of the current individual's chromosome
        with those of another parent.

        :param parent2: The second parent individual.
        :return: A new Individual instance.
        """
        start = self.n_genes // 3
        random_a = self._get_random_int(start, self.n_genes)

        new_chromosome = self.chromosome[:]
        for i in range(random_a, self.n_genes):
            new_chromosome[i] = parent2.at(i)

        return Individual(chromosome=new_chromosome)


    def insert_color(self, p, c):
        """
        Inserts a specific color at a given position in the chromosome.

        :param p: The position in the chromosome.
        :param c: The color to insert.
        """
        self.chromosome[p] = c


    def _get_random_int(self, start, end):
        """
        Generates a random integer between the given range.

        :param start: The starting value (inclusive).
        :param end: The ending value (inclusive).
        :return: A random integer within the range.
        """
        return random.randint(start, end)
    
    def save_coloring_to_file(self, filename,best_solution):
            """
            Save the current best solution's coloring to a file in the specified format.

            :param filename: Name of the file to save the coloring.
            """
            with open(filename, 'w') as file:
                # Write the chromosome in the same format as it is printed
                file.write(f"Chromosome: {best_solution.chromosome} \nNumber of colors used: {best_solution.get_num_of_colors()}\nFitness: {best_solution.get_fitness()}\n")
                print(f"Best solution saved to {filename}")
        