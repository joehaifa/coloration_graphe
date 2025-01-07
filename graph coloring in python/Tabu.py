


from collections import deque
import os
from Individual import Individual

import random

from collections import Counter

class Tabu:
    def __init__(self, neighborhood_size, n_nodes, n_edges, main_graph, n_colors):
        self.neighborhood_size = neighborhood_size
        self.n_nodes = n_nodes
        self.n_edges = n_edges
        self.main_graph = main_graph
        self.n_colors = n_colors
        self.tabu_size = max(n_edges // 4, 10)
        self.tabu_list = []
        self.best_solution = None
        self.current_solution = self.generate_initial_solution()
        self.best_conflicts = float('inf')
        self.no_improvement_count = 0

    def generate_initial_solution(self):
        """
        Génère une solution initiale aléatoire avec un grand nombre de couleurs.
        """
        individual = Individual(n_genes=self.n_nodes, n_colors=self.n_colors)
        self.calculate_fitness(individual)
        return individual

    def find_conflicts(self, chromosome):
        """
        Retourne une liste des nœuds en conflit et le nombre total de conflits.
        """
        conflicts = []
        total_conflicts = 0
        for node in range(self.n_nodes):
            for neighbor in self.main_graph[node]:
                if chromosome[node] == chromosome[neighbor]:
                    conflicts.append(node)
                    total_conflicts += 1
                    break
        return conflicts, total_conflicts

    def calculate_fitness(self, individual):
        """
        Calcule la fitness basée sur le nombre de conflits.
        """
        _, total_conflicts = self.find_conflicts(individual.chromosome)
        fitness = -(2 * total_conflicts) + (self.n_nodes - individual.get_num_of_colors())
        individual.set_fitness(fitness)
        return fitness

    def apply_best_move(self):
        """
        Explore les voisins et applique le meilleur mouvement non-tabu.
        """
        conflicts, _ = self.find_conflicts(self.current_solution.chromosome)
        if not conflicts:
            return  # Pas de conflits à résoudre

        best_move = None
        best_fitness = float('-inf')
        best_chromosome = self.current_solution.chromosome[:]

        for node in conflicts:
            for color_candidate in range(self.n_colors):
                if self.current_solution.chromosome[node] != color_candidate:
                    if self.check_tabu_list(node, color_candidate):
                        continue

                    # Tester le changement
                    temp_chromosome = self.current_solution.chromosome[:]
                    temp_chromosome[node] = color_candidate
                    temp_individual = Individual(self.n_nodes, self.n_colors)
                    temp_individual.chromosome = temp_chromosome

                    new_fitness = self.calculate_fitness(temp_individual)

                    # Mettre à jour la meilleure solution
                    if new_fitness > best_fitness:
                        best_fitness = new_fitness
                        best_move = (node, color_candidate)
                        best_chromosome = temp_chromosome

        if best_move:
            node, color = best_move
            if len(self.tabu_list) >= self.tabu_size:
                self.tabu_list.pop(0)
            self.tabu_list.append((node, self.current_solution.chromosome[node]))

            # Appliquer le mouvement
            self.current_solution.chromosome = best_chromosome
            self.current_solution.set_fitness(best_fitness)

    def check_tabu_list(self, node, color):
        """
        Vérifie si un mouvement est dans la liste tabu.
        """
        return (node, color) in self.tabu_list

    def diversify_solution(self):
        """
        Introduit des perturbations aléatoires dans la solution actuelle.
        """
        for node in range(self.n_nodes):
            if random.random() < 0.2:  # 20% de chance de mutation
                self.current_solution.chromosome[node] = random.randint(0, self.n_colors - 1)

    def main_loop(self, max_iterations, min_colors,totaliteration):
        """
        Boucle principale de l'algorithme Tabu.
        """
        for iteration in range(max_iterations):
            totaliteration[0]+=1
            self.apply_best_move()
            conflicts, total_conflicts = self.find_conflicts(self.current_solution.chromosome)

            # Mettre à jour la meilleure solution
            if total_conflicts < self.best_conflicts:
                self.best_conflicts = total_conflicts
                self.best_solution = self.current_solution
                self.no_improvement_count = 0
            else:
                self.no_improvement_count += 1

            # Si aucune amélioration après plusieurs itérations, diversifier
            if self.no_improvement_count > 50:
                self.diversify_solution()
                self.no_improvement_count = 0

            # Réduire le nombre de couleurs si possible
            if not conflicts and self.current_solution.get_num_of_colors() > min_colors:
                self.n_colors -= 1
                self.current_solution = self.generate_initial_solution()

            # Si aucune amélioration et aucun conflit, terminer
            if not conflicts and self.current_solution.get_num_of_colors() <= min_colors:
                break

        # Afficher les résultats
        if self.best_solution:
            print("\nBest Solution:")
            print(f"Chromosome : {self.best_solution.chromosome}")
            print(f"Nombre de couleurs : {self.best_solution.get_num_of_colors()}")
            print(f"FIT : {self.best_solution.get_fitness()}")
            self.save_best_solution()
        else:
            print("Aucune solution optimale trouvée.")

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



from collections import deque
import os
from Individual import Individual

import random

from collections import Counter

class Tabu:
    def __init__(self, neighborhood_size, n_nodes, n_edges, main_graph, n_colors):
        self.neighborhood_size = neighborhood_size
        self.n_nodes = n_nodes
        self.n_edges = n_edges
        self.main_graph = main_graph
        self.n_colors = n_colors
        self.tabu_size = max(n_edges // 4, 10)
        self.tabu_list = []
        self.best_solution = None
        self.current_solution = self.generate_initial_solution()
        self.best_conflicts = float('inf')
        self.no_improvement_count = 0

    def generate_initial_solution(self):
        """
        Génère une solution initiale aléatoire avec un grand nombre de couleurs.
        """
        individual = Individual(n_genes=self.n_nodes, n_colors=self.n_colors)
        self.calculate_fitness(individual)
        return individual

    def find_conflicts(self, chromosome):
        """
        Retourne une liste des nœuds en conflit et le nombre total de conflits.
        """
        conflicts = []
        total_conflicts = 0
        for node in range(self.n_nodes):
            for neighbor in self.main_graph[node]:
                if chromosome[node] == chromosome[neighbor]:
                    conflicts.append(node)
                    total_conflicts += 1
                    break
        return conflicts, total_conflicts

    def calculate_fitness(self, individual):
        """
        Calcule la fitness basée sur le nombre de conflits.
        """
        _, total_conflicts = self.find_conflicts(individual.chromosome)
        fitness = -(2 * total_conflicts) + (self.n_nodes - individual.get_num_of_colors())
        individual.set_fitness(fitness)
        return fitness

    def apply_best_move(self):
        """
        Explore les voisins et applique le meilleur mouvement non-tabu.
        """
        conflicts, _ = self.find_conflicts(self.current_solution.chromosome)
        if not conflicts:
            return  # Pas de conflits à résoudre

        best_move = None
        best_fitness = float('-inf')
        best_chromosome = self.current_solution.chromosome[:]

        for node in conflicts:
            for color_candidate in range(self.n_colors):
                if self.current_solution.chromosome[node] != color_candidate:
                    if self.check_tabu_list(node, color_candidate):
                        continue

                    # Tester le changement
                    temp_chromosome = self.current_solution.chromosome[:]
                    temp_chromosome[node] = color_candidate
                    temp_individual = Individual(self.n_nodes, self.n_colors)
                    temp_individual.chromosome = temp_chromosome

                    new_fitness = self.calculate_fitness(temp_individual)

                    # Mettre à jour la meilleure solution
                    if new_fitness > best_fitness:
                        best_fitness = new_fitness
                        best_move = (node, color_candidate)
                        best_chromosome = temp_chromosome

        if best_move:
            node, color = best_move
            if len(self.tabu_list) >= self.tabu_size:
                self.tabu_list.pop(0)
            self.tabu_list.append((node, self.current_solution.chromosome[node]))

            # Appliquer le mouvement
            self.current_solution.chromosome = best_chromosome
            self.current_solution.set_fitness(best_fitness)

    def check_tabu_list(self, node, color):
        """
        Vérifie si un mouvement est dans la liste tabu.
        """
        return (node, color) in self.tabu_list

    def diversify_solution(self):
        """
        Introduit des perturbations aléatoires dans la solution actuelle.
        """
        for node in range(self.n_nodes):
            if random.random() < 0.2:  # 20% de chance de mutation
                self.current_solution.chromosome[node] = random.randint(0, self.n_colors - 1)

    def main_loop(self, max_iterations, min_colors,totaliteration):
        """
        Boucle principale de l'algorithme Tabu.
        """
        for iteration in range(max_iterations):
            totaliteration[0]+=1
            self.apply_best_move()
            conflicts, total_conflicts = self.find_conflicts(self.current_solution.chromosome)

            # Mettre à jour la meilleure solution
            if total_conflicts < self.best_conflicts:
                self.best_conflicts = total_conflicts
                self.best_solution = self.current_solution
                self.no_improvement_count = 0
            else:
                self.no_improvement_count += 1

            # Si aucune amélioration après plusieurs itérations, diversifier
            if self.no_improvement_count > 50:
                self.diversify_solution()
                self.no_improvement_count = 0

            # Réduire le nombre de couleurs si possible
            if not conflicts and self.current_solution.get_num_of_colors() > min_colors:
                self.n_colors -= 1
                self.current_solution = self.generate_initial_solution()

            # Si aucune amélioration et aucun conflit, terminer
            if not conflicts and self.current_solution.get_num_of_colors() <= min_colors:
                break

        # Afficher les résultats
        if self.best_solution:
            print("\nBest Solution:")
            print(f"Chromosome : {self.best_solution.chromosome}")
            print(f"Nombre de couleurs : {self.best_solution.get_num_of_colors()}")
            print(f"FIT : {self.best_solution.get_fitness()}")
            print(f"Conflits : {self.best_conflicts}")
            self.save_best_solution()
        else:
            print("Aucune solution optimale trouvée.")

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
