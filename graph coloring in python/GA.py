import random
from Individual import Individual
import os 

class GA:
    def __init__(self, graph, population_size, n_colors, mutation_rate):
        self.graph = graph
        self.population_size = population_size
        self.n_colors = n_colors
        self.mutation_rate = mutation_rate
        self.population = [Individual(len(graph), n_colors) for _ in range(population_size)]
        self.best_solution = None  # Stocker la meilleure solution trouvée

    def fitness(self, individual):
        """ Calculate fitness by penalizing conflicts and rewarding fewer colors. """
        conflicts = 0
        for node in range(len(self.graph)):
            for neighbor in self.graph[node]:
                if individual.chromosome[node] == individual.chromosome[neighbor]:
                    conflicts += 1
        # Reward solutions with fewer colors
        return -conflicts + (len(self.graph) - individual.get_num_of_colors())

    def select_parents(self):
        """ Select two parents using tournament selection. """
        tournament = random.sample(self.population, k=3)
        tournament.sort(key=lambda ind: self.fitness(ind), reverse=True)
        return tournament[0], tournament[1]

    def crossover(self, parent1, parent2):
        """ Perform uniform crossover between two parents. """
        child = Individual(len(self.graph), self.n_colors)
        child.chromosome = [
            random.choice([parent1.chromosome[i], parent2.chromosome[i]])
            for i in range(len(self.graph))
        ]
        return child

    def correct_conflicts(self, individual):
        """ Resolve conflicts in an individual's coloring. """
        for node, neighbors in enumerate(self.graph):
            neighbor_colors = {individual.chromosome[neighbor] for neighbor in neighbors}
            if individual.chromosome[node] in neighbor_colors:
                for color in range(self.n_colors):
                    if color not in neighbor_colors:
                        individual.chromosome[node] = color
                        break

    def no_conflicts(self, individual):
        """ Check if an individual's coloring is conflict-free. """
        for node, neighbors in enumerate(self.graph):
            for neighbor in neighbors:
                if individual.chromosome[node] == individual.chromosome[neighbor]:
                    return False
        return True

    def evolve(self):
        """ Create the next generation of individuals. """
        new_population = []
        for _ in range(self.population_size):
            parent1, parent2 = self.select_parents()
            child = self.crossover(parent1, parent2)
            if random.random() < self.mutation_rate:
                child.mutate(self.graph)
            self.correct_conflicts(child)  # Correct conflicts after mutation
            new_population.append(child)
        self.population = new_population

    def save_best_solution(self):
            """
            Save the best solution's coloring to a file in the same directory as the script.
            """
            # Get the directory of the main script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "best_solution.txt")

            try:
                with open(file_path, 'w') as file:
                    file.write(f"Chromosome: {self.best_solution.chromosome}\n")
                    file.write(f"Number of colors used: {self.best_solution.get_num_of_colors()}\n")
                    file.write(f"Fitness: {self.fitness(self.best_solution)}\n")
                print(f"Best solution saved successfully to {file_path}.")
            except IOError as e:
                print(f"Error writing to file: {e}")

    def run(self, max_generations,totaliteration):
        """ Run the genetic algorithm. """
        for generation in range(max_generations):
            totaliteration[0]+=1
            self.population.sort(key=lambda ind: self.fitness(ind), reverse=True)
            best_individual = self.population[0]

            # Mettre à jour la meilleure solution si nécessaire
            if not self.best_solution or self.fitness(best_individual) > self.fitness(self.best_solution):
                self.best_solution = best_individual

            # Check if the best solution is conflict-free
            if self.no_conflicts(best_individual):
                print(f"Generation {generation}: Best fitness = {self.fitness(best_individual)}")
                print(f"Conflict-free solution found in generation {generation}.")
                self.save_best_solution()
                return best_individual

            
            self.evolve()

        # Save the best solution after all generations
        self.population.sort(key=lambda ind: self.fitness(ind), reverse=True)
        self.best_solution = self.population[0]
        self.save_best_solution(output_file)
        return self.best_solution
