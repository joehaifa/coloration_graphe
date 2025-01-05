import random
import math
from Individual import Individual
import os


class SA:
    def __init__(self, initial_temperature, n_nodes, n_edges, main_graph, min_colors, cool_mode=0, alpha=0.005):
        self.temperature = self.temperature0 = initial_temperature
        self.cool_mode = cool_mode
        self.alpha = alpha
        self.main_graph = main_graph
        self.n_nodes = n_nodes
        self.n_edges = n_edges
        self.min_colors = min_colors
        self.n_colors = max(min_colors, 10)

        # Generate a greedy initial solution
        self.generate_greedy_solution()

    def generate_greedy_solution(self):
        """Generate an initial solution using a greedy coloring heuristic."""
        colors = [-1] * self.n_nodes
        for node in range(self.n_nodes):
            # Get colors of neighbors
            neighbor_colors = {colors[neighbor] for neighbor in self.main_graph[node] if colors[neighbor] != -1}
            # Assign the smallest available color
            for color in range(self.n_colors):
                if color not in neighbor_colors:
                    colors[node] = color
                    break
        new_individual = Individual(n_genes=self.n_nodes, n_colors=self.n_colors)
        new_individual.chromosome = colors
        self.current_solution = new_individual
        self.best_solution = new_individual

    def get_best_state(self):
        return self.best_solution

    def find_first_collision(self):
        for i in range(self.n_nodes):
            for neighbor in self.main_graph[i]:
                if self.current_solution.at(i) == self.current_solution.at(neighbor):
                    return i
        return random.randint(0, self.n_nodes - 1)

    def next_neighbor(self):
        node = self.find_first_collision()

        # Get available colors for this node
        used_colors = {self.current_solution.at(neighbor) for neighbor in self.main_graph[node]}
        available_colors = [c for c in range(self.n_colors) if c not in used_colors]

        # Assign a random valid color or fallback to random
        color = random.choice(available_colors) if available_colors else random.randint(0, self.n_colors - 1)

        temp_solution = Individual(n_genes=self.n_nodes, n_colors=self.n_colors)
        temp_solution.chromosome = self.current_solution.chromosome[:]
        temp_solution.insert_color(node, color)

        temp_fit = self.calculate_fitness(temp_solution)
        current_fit = self.calculate_fitness(self.current_solution)

        # Always accept better solutions
        if temp_fit > current_fit:
            self.current_solution = temp_solution
        else:
            # Accept worse solutions based on temperature
            diff_fitness = current_fit - temp_fit
            if random.random() < math.exp(-diff_fitness / self.temperature):
                self.current_solution = temp_solution

    def cool(self, k):
        """Cooling schedule."""
        if self.cool_mode == 0:
            self.temperature -= self.alpha
        elif self.cool_mode == 1:
            self.temperature *= (1 - self.alpha)  # Exponential cooling
        else:
            self.temperature = self.temperature0 / math.log(k + 2)

    def main_loop(self, max_iterations, min_temp, total_iterations):
        correct = 0

        for total_iterations[0] in range(max_iterations):
            self.next_neighbor()
            self.cool(total_iterations[0])

            # Stop if the temperature is below the minimum
            if self.temperature < min_temp:
                break

            # Update the best solution if a better one is found
            if self.current_solution.get_fitness() > self.best_solution.get_fitness():
                self.best_solution = self.current_solution

            # Check if the solution is conflict-free
            if self.current_solution.get_fitness() == self.n_edges and self.current_solution.get_num_of_colors() <= self.min_colors:
                correct += 1
            else:
                correct = 0

            # Ensure no conflicts for termination
            if correct == 10 and self.is_conflict_free(self.current_solution):
                break

        # Save the best solution to a file
        self.best_solution.save_best_solution( self.best_solution)

    def calculate_fitness(self, ind):
        """Fitness function to evaluate a solution."""
        fit = 0
        conflicts = 0
        for i in range(self.n_nodes):
            for neighbor in self.main_graph[i]:
                if ind.at(i) != ind.at(neighbor):
                    fit += 1
                else:
                    conflicts += 1

        # Strong penalty for conflicts
        conflict_penalty = conflicts * 10

        # Penalty for exceeding the minimum number of colors
        color_penalty = max(0, (ind.get_num_of_colors() - self.min_colors) * 20)

        # Reward for fewer colors if conflict-free
        if conflicts == 0:
            fit += (self.n_nodes - ind.get_num_of_colors()) * 10

        fit -= conflict_penalty + color_penalty
        ind.set_fitness(fit)
        return fit

    def is_conflict_free(self, ind):
        """Check if a solution is conflict-free."""
        for i in range(self.n_nodes):
            for neighbor in self.main_graph[i]:
                if ind.at(i) == ind.at(neighbor):
                    return False
        return True
