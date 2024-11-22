import random
import math
from Individual import Individual

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
        return self.best_solution

    def find_first_collision(self):
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
        self.best_solution.save_coloring_to_file("best_solution.txt",self.best_solution)

    def calculate_fitness(self, ind):
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

    
