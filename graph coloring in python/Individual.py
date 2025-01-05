import random
import os
class Individual:
    def __init__(self, n_genes, n_colors):
        self.chromosome = [random.randint(0, n_colors - 1) for _ in range(n_genes)]
        self.n_colors = n_colors
        self.fitness = 0

    def get_num_of_colors(self):
        return len(set(self.chromosome))

    



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


    def mutate(self, graph):
        """ Mutate nodes causing conflicts. """
        for node in range(len(self.chromosome)):
            for neighbor in graph[node]:
                if self.chromosome[node] == self.chromosome[neighbor]:
                    self.chromosome[node] = random.choice(
                        [color for color in range(self.n_colors) if color != self.chromosome[node]] )



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
    
    def save_best_solution(self,best_solution):
            """
            Save the best solution's coloring to a file in the same directory as the script.
            """
            # Get the directory of the main script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "best_solution.txt")

            try:
                with open(file_path, 'w') as file:
                    file.write(f"Chromosome: {best_solution.chromosome}\n")
                    file.write(f"Number of colors used: {best_solution.get_num_of_colors()}\n")
                    file.write(f"Fitness: {best_solution.get_fitness()}\n")
                print(f"Best solution saved successfully to {file_path}.")
            except IOError as e:
                print(f"Error writing to file: {e}")
        
