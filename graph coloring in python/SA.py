import random
import math
from Individual import Individual
import os

class SA:

    def __init__(self, initial_temperature, n_nodes, n_edges, main_graph, cool_mode=0, alpha=0.005):
        self.temperature = self.temperature0 = initial_temperature
        self.cool_mode = cool_mode
        self.alpha = alpha
        self.main_graph = main_graph
        self.n_nodes = n_nodes
        self.n_edges = n_edges

        # Create an Individual with a chromosome initialized to 1 for each gene
        chromosome = [1] * n_nodes
        new_individual = Individual(chromosome=chromosome)
        self.best_solution = new_individual
        self.current_solution = new_individual


    def get_best_state(self):
        """
        Returns the best solution found during the SA process.

        :return: The best solution as an Individual object.
        """
        return self.best_solution


    def find_first_collision(self):
        """
        Identifies the first node with a color conflict in the current solution.

        :return: The index of the conflicting node, or a random node if no conflicts exist.
        """
        pos_collision = -1
        collision = False

        if self.current_solution.get_fitness() < self.n_edges:
            for i in range(self.n_nodes):
                for pos in self.main_graph[i]:
                    if self.current_solution.at(i) == self.current_solution.at(pos):
                        pos_collision = i
                        collision = True
                        break
                if collision:
                    break
        
        if not collision:
            pos_collision = random.randint(0, self.n_nodes - 1)
        
        return pos_collision


    def next_neighbor(self):
        """
        Generates the next neighbor by modifying the color of a conflicting node
        and decides whether to accept the new solution based on fitness and temperature.
        """
        node = self.find_first_collision()

        # Instead of assigning a random color, try to find a color that minimizes conflicts
        available_colors = set(range(self.n_nodes))
        for neighbor in self.main_graph[node]:
            if self.current_solution.at(neighbor) in available_colors:
                available_colors.remove(self.current_solution.at(neighbor))

        # Choose a color from the remaining set or a random color if all are used
        color = random.choice(list(available_colors)) if available_colors else random.randint(0, self.n_nodes - 1)

        # Copy current_solution to temp_solution for mutation
        temp_solution = Individual(chromosome=self.current_solution.chromosome[:])
        temp_solution.insert_color(node, color)
        temp_solution.set_fitness(0)

        temp_fit = self.calculate_fitness(temp_solution)
        current_fit = self.calculate_fitness(self.current_solution)

        if temp_fit > current_fit:
            self.current_solution = temp_solution
        else:
            p = random.random()
            diff_fitness = current_fit - temp_fit

            if p < math.exp(-diff_fitness / self.temperature):
                self.current_solution = temp_solution

    def cool(self, k):
        """
        Reduces the temperature based on the selected cooling mode.

        :param k: The current iteration number.
        """
        if self.cool_mode == 0:
            self.temperature -= self.alpha
        elif self.cool_mode == 1:
            self.temperature *= self.alpha
        else:
            self.temperature = self.temperature0 / math.log(k + 2)


    def main_loop(self, max_iterations, min_temp, min_colors,totaliteration):
        correct = 0
        correct_color = False

        for totaliteration[0] in range(max_iterations):
            self.next_neighbor()
            self.cool(totaliteration[0])

            if self.temperature < min_temp:
                break

            if self.current_solution.get_fitness() > self.best_solution.get_fitness():
                self.best_solution = self.current_solution

            if self.current_solution.get_num_of_colors() == min_colors:
                correct += 1

            if correct == 10:
                correct_color = True
                break

        # Save the best solution to a file
        self.save_best_solution()


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
                file.write(f"Fitness: {self.best_solution.get_fitness()}\n")
            print(f"Best solution saved successfully to {file_path}.")
        except IOError as e:
            print(f"Error writing to file: {e}")


    def calculate_fitness(self, ind):
        """
        Calculates the fitness of an individual solution based on the number of
        non-conflicting edges and penalizes the number of colors used.

        :param ind: The individual whose fitness is being calculated.
        :return: The calculated fitness value.
        """
        fit = ind.get_fitness()

        if fit == 0:
            fit = 0
            for i in range(self.n_nodes):
                for j in self.main_graph[i]:
                    if ind.at(i) != ind.at(j):
                        fit += 1

            if fit == self.n_edges:
                fit += (self.n_nodes - ind.get_num_of_colors())

            ind.set_fitness(fit)
        
        return fit

    
