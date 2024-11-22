import random
from collections import deque
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
        individual = Individual(n_genes=self.n_nodes)  # Use 'n_genes' instead of 'nGenes'
        for i in range(self.n_nodes):
            individual.insert_color(i, random.randint(0, self.n_nodes // 2))  # Use half the number of colors
        self.calculate_fitness(individual)
        return individual
    
    def find_first_collision(self):
        for i in range(self.n_nodes):
            for neighbor in self.main_graph[i]:
                if self.current_solution.at(i) == self.current_solution.at(neighbor):
                    return i
        return -1
    
    def check_tabu_list(self, p, c):
        return (p, c) in self.tabu_list
    
    def next_neighbor(self):
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
    
    def main_loop(self, max_iterations, min_colors,totaliteration):
        for iteration in range(max_iterations):
            totaliteration[0]+=1
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
        self.best_solution.save_coloring_to_file("best_solution.txt",self.best_solution)

    def calculate_fitness(self, ind):
        non_conflicting_edges = sum(1 for i in range(self.n_nodes) 
                                    for neighbor in self.main_graph[i] 
                                    if ind.at(i) != ind.at(neighbor)) // 2  # Count each edge once
        colors_penalty = self.n_nodes - ind.get_num_of_colors()
        fitness = non_conflicting_edges + colors_penalty
        ind.set_fitness(fitness)
        return fitness
    
