import random
from collections import deque
import os
from Individual import Individual

class Tabu:
    def __init__(self, neighborhood_size, n_nodes, n_edges, main_graph):
        self.neighborhood_size = neighborhood_size
        self.n_nodes = n_nodes
        self.n_edges = n_edges
        self.main_graph = main_graph
        self.tabu_size = max(n_edges // 4, 1)
        new_individual = self.generate_initial_solution()
        self.best_solution = self.current_solution = new_individual
        self.critical_solutions = []
        self.tabu_list = []
    

    def generate_initial_solution(self):
        """
        Generates an initial solution by assigning random colors to each node.
        """
        individual = Individual(n_genes=self.n_nodes)  # Use 'n_genes' instead of 'nGenes'
        for i in range(self.n_nodes):
            individual.insert_color(i, random.randint(0, self.n_nodes // 2))  # Use half the number of colors
        self.calculate_fitness(individual)
        return individual
    

    def find_first_collision(self):
        """
        Finds the first node in the graph that has a color conflict with its neighbors.

        :return: The index of the conflicting node, or -1 if no conflicts are found.
        """
        for i in range(self.n_nodes):
            for neighbor in self.main_graph[i]:
                if self.current_solution.at(i) == self.current_solution.at(neighbor):
                    return i
        return -1
    

    def check_tabu_list(self, p, c):
        """
        Checks if a move (node, color) is in the tabu list.

        :param p: The node index.
        :param c: The proposed color.
        :return: True if the move is tabu, False otherwise.
        """
        return (p, c) in self.tabu_list
    

    def next_neighbor(self):
        """
        Finds and applies the best non-tabu move to reduce conflicts or improve fitness.
        """
        node = self.find_first_collision()
        if node == -1:
            return  # No collision
        
        best_neighbor = self.current_solution
        best_fitness = self.current_solution.get_fitness()
        best_move = None
        
        for color_candidate in range(self.n_nodes):
            conflict = any(self.current_solution.at(neighbor) == color_candidate for neighbor in self.main_graph[node])
            if not conflict:
                best_neighbor.insert_color(node, color_candidate)
                new_fitness = self.calculate_fitness(best_neighbor)
                if new_fitness > best_fitness:
                    best_fitness = new_fitness
                    best_move = (node, color_candidate)
        
        if best_move:
            if len(self.tabu_list) >= self.tabu_size:
                self.tabu_list.pop(0)
            self.tabu_list.append(best_move)
            self.current_solution = best_neighbor
            self.current_solution.set_fitness(best_fitness)
    

    def main_loop(self, max_iterations, min_colors, totaliteration):
        for iteration in range(max_iterations):
            totaliteration[0] += 1
            self.calculate_fitness(self.current_solution)
            if self.current_solution.get_num_of_colors() <= min_colors:
                break
            self.next_neighbor()
            if self.current_solution.get_fitness() > self.best_solution.get_fitness():
                self.best_solution = self.current_solution
                self.critical_solutions.append(self.best_solution)
        
        print("\nBest Solution:")
        self.best_solution.print_chromosome()
        print(f"FIT: {self.best_solution.get_fitness()}")
        
        # Save the best solution coloring to a file
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
        non-conflicting edges and the number of colors used.

        :param ind: The individual whose fitness is to be calculated.
        :return: The fitness value.
        """
        non_conflicting_edges = sum(1 for i in range(self.n_nodes) 
                                    for neighbor in self.main_graph[i] 
                                    if ind.at(i) != ind.at(neighbor)) // 2  # Count each edge once
        colors_penalty = self.n_nodes - ind.get_num_of_colors()
        fitness = non_conflicting_edges + colors_penalty
        ind.set_fitness(fitness)
        return fitness
    
