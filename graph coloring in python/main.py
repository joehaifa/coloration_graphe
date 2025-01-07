import time
from typing import List
import sys
from Individual import Individual
from GA import GA
from Tabu import Tabu
from SA import SA
import os

class Graph:
    def __init__(self):
        self.graph = []
        self.n_nodes = 0
        self.n_edges = 0

    def load_graph(self, graph_name: str) -> bool:
        """
        Loads a graph from a file in the standard 'p edge' format and stores it as an adjacency list.
        """
        # Dynamically construct the path relative to the current script location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "data", f"{graph_name}.txt")

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith("p edge"):
                        parts = line.split()
                        self.n_nodes = int(parts[2])
                        self.n_edges = int(parts[3])
                        self.graph = [[] for _ in range(self.n_nodes)]
                    elif line.startswith("e"):
                        parts = line.split()
                        node1 = int(parts[1]) - 1
                        node2 = int(parts[2]) - 1
                        self.graph[node1].append(node2)
            print(f"Graph '{graph_name}' loaded successfully from {file_path}.")
            return True
        except IOError as e:
            print(f"Can't open the file: {e}")
            return False

    def load_colored_graph(self, graph_name: str) -> dict:
        """
        Loads a graph from a .col file, returning the adjacency list as a dictionary.
        It also adapts the function to handle dynamic graph sizes.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "data", f"{graph_name}.col.txt")
        
        adjacency_list = {}  # Initialize the adjacency list as a dictionary
        
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith("p edge"):
                        parts = line.split()
                        self.n_nodes = int(parts[2])
                        self.n_edges = int(parts[3])
                        adjacency_list = {i: [] for i in range(self.n_nodes)}  # Initialize nodes
                    elif line.startswith("e"):
                        parts = line.split()
                        node1 = int(parts[1]) - 1  # Adjust to 0-based index
                        node2 = int(parts[2]) - 1
                        adjacency_list[node1].append(node2) # Add edge
                      
                        
                        
            
            print("Graph loaded successfully.")
            return adjacency_list
        except IOError as e:
            print(f"Can't open the file path: {e}")
            return None

    def save_graph(self, file_name: str):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "data")

        # Ensure the 'data' directory exists
        os.makedirs(data_dir, exist_ok=True)

        # Construct the file path
        file_path = os.path.join(data_dir, f"{file_name}.txt")
        try:
            with open(file_path, 'w') as file:
                # Write the graph metadata (nodes and edges)
                file.write(f"p edge {self.n_nodes} {self.n_edges}\n")
                for node1, neighbors in enumerate(self.graph):
                    for node2 in neighbors:
                        file.write(f"e {node1 + 1} {node2 + 1}\n")
            print("Graph saved successfully.")
        except IOError as e:
            print(f"Error writing to file: {e}")

    def print_graph(self):
        if not self.graph:
            print("The graph is not loaded.")
        else:
            for i, neighbors in enumerate(self.graph):
                print(f"\n[{i}] ->", " ".join(map(str, neighbors)))
            print()

    def get_nodes(self):
        return self.n_nodes

    def get_edges(self):
        return self.n_edges

    def get_graph(self):
        return self.graph

def modify_graph(graph: Graph):
    print("\nSelect a graph to modify:")
    graph_files = ["myciel3.col", "myciel4.col","DSJC125.1.col","anna.col","queen9_9.col"]
    for i, filename in enumerate(graph_files):
        print(f"[{i}] {filename}")
    graph_index = int(input("Enter your choice: "))
    graph_name = graph_files[graph_index]
    

    # Load the selected graph
    if not graph.load_graph(graph_name):
        print("The graph did not load.")
        return
    graph.print_graph()
    # Ask if the user wants to add or remove an edge
    print("\nDo you want to add or remove an edge?")
    print("1. Add an edge")
    print("2. Remove an edge")
    action = int(input("Enter your choice: "))

    if action == 1:
        node1 = int(input("Enter the first node : ")) 
        node2 = int(input("Enter the second node : "))
        # Ensure no duplicate edges (bidirectional check)
        if node2 in graph.get_graph()[node1] or node1 in graph.get_graph()[node2]:
            print(f"Connection between Node {node1} and Node {node2} already exists.")
        else:
            if(node1<node2):
                graph.get_graph()[node1].append(node2)
            else:
                graph.get_graph()[node2].append(node1)
            
            graph.n_edges += 1
            print(f"Edge between Node {node1} and Node {node2} added successfully.")
    
    elif action == 2:
        node1 = int(input("Enter the first node : ")) 
        node2 = int(input("Enter the second node : "))
        # Ensure no duplicate edges (bidirectional check)
        if node2 in graph.get_graph()[node1] or node1 in graph.get_graph()[node2]:
            # Remove the edge in both directions
            if(node2 in graph.get_graph()[node1]):
                graph.get_graph()[node1].remove(node2)
            else:
                graph.get_graph()[node2].remove(node1)
        
            graph.n_edges -= 1
            print(f"Edge between Node {node1} and Node {node2} removed successfully.")
        else:
            print(f"No connection found between Node {node1} and Node {node2}.")

    
    else:
        print("Invalid option selected.")
        return

    # Save the updated graph back to the file
    graph.save_graph(graph_name)
    graph.print_graph()



    

    

    
    
    




    
    

def read_coloring_from_file(file_path):
    """
    Lit une coloration depuis un fichier et la retourne sous forme de dictionnaire.
    
    :param file_path: Le chemin du fichier contenant la coloration.
    :return: Dictionnaire représentant la coloration sous forme {sommet: couleur}.
    """
    coloring = {}

    with open(file_path, 'r') as file:
        # Lire le contenu du fichier
        lines = file.readlines()

        # Trouver la ligne contenant la chromosome et l'analyser
        for line in lines:
            if line.startswith("Chromosome:"):
                # Extraire la liste des couleurs du chromosome
                start_idx = line.index('[') + 1
                end_idx = line.index(']')
                chromosome_str = line[start_idx:end_idx]
                
                # Convertir la chaîne en liste d'entiers
                chromosome = list(map(int, chromosome_str.split(',')))

                # Construire le dictionnaire de la coloration
                for idx, color in enumerate(chromosome):
                    coloring[idx] = color

    return coloring
    

def check_coloring(adjacency_list, coloring):
    """
    Checks if the given coloring of a graph has any conflicts.

    :param adjacency_list: A dictionary where each key is a node, and the value is a list of adjacent nodes.
    :param coloring: A dictionary where each key is a node, and the value is the assigned color for that node.
    :return: A list of conflicting nodes, or an empty list if there are no conflicts.
    """
    conflicts = []
    
    for node, neighbors in adjacency_list.items():
        node_color = coloring[node]
        for neighbor in neighbors:
            if coloring[neighbor] == node_color:
                conflicts.append((node, neighbor))
    
    if conflicts:
        print("Conflicts found between the following nodes:")
        for conflict in conflicts:
            print(f"Node {conflict[0]} and Node {conflict[1]} both have color {coloring[conflict[0]]}")
    else:
        print("No conflicts found in the coloring.")
        
    return conflicts


def main():
    print("Select an option:")
    print("1. Color a graph")
    print("2. Propose a coloring")
    print("3. Modify a graph")
    print("4. QUIT")

    option = int(input("Enter your choice: "))

    if option == 1:
        # Existing code for "Color a graph"
        data = ["myciel3.col", "myciel4.col","DSJC125.1.col","anna.col","queen9_9.col"]
        graph_main = Graph()

        # Graph selection
        if len(sys.argv) < 2:
            print("Select a graph from the list:")
            for i, name in enumerate(data):
                print(f" [{i}] {name}")
            n_graph = int(input("Enter a number: "))
        elif len(sys.argv) > 2:
            print("Too many arguments.")
            return
        else:
            n_graph = int(sys.argv[1])

        if n_graph >= len(data):
            print("Not a valid graph.")
        elif not graph_main.load_graph(data[n_graph]):
            print("The graph did not load.")
            return
        else:
            graph_main.print_graph()

        

        # Solving method selection
        print("Now, choose a solving method: \n1. Genetic Algorithm \n2. Simulated Annealing \n3. Tabu Search")
        select_method = int(input())

        max_iterations = 100000
        totaliteration = [0] 
        start_time = time.time()
        if select_method == 1:
            # Genetic Algorithm parameters
            max_iterations = 10000
            n_individuals = 20
            p_best = 40.0
            p_cross = 40.0
            p_mutation = 20.0
            n_colors = 0

            if n_graph == 0:
                max_iterations = 1000
                n_individuals = 10
                n_colors = 4

            if n_graph == 1:
                max_iterations = 1000
                n_individuals = 10
                n_colors = 5
            
            if n_graph == 2:
                max_iterations = 1000
                n_individuals = 10
                n_colors = 7

            if n_graph == 3:
                max_iterations = 1000
                n_individuals = 10
                n_colors = 11
            
            if n_graph == 4:
                max_iterations = 1000
                n_individuals = 10
                n_colors = 13
            
          
            

            
            

                
            ga = GA(graph_main.get_graph(), population_size=100, n_colors=n_colors , mutation_rate=0.1)
            best_solution = ga.run(max_generations=1000,totaliteration=totaliteration)

            print(f"Best solution found: {best_solution.chromosome}")
            print(f"Number of colors used: {best_solution.get_num_of_colors()}")

        elif select_method == 2:
            # Simulated Annealing parameters
            max_iterations = 10000
            initial_temp = 1.0
            n_colors = 0
            min_temp = 0
    
            
            if n_graph == 0:
                n_colors = 4
                initial_temp = 1.0
                min_temp = 0.1

            if n_graph == 1:
                n_colors = 5
            
            if n_graph == 2:
                n_colors = 8

            if n_graph == 3:
                n_colors = 11
            
            if n_graph == 4:
                n_colors = 13

           


            sa_solution = SA(initial_temp, graph_main.get_nodes(), graph_main.get_edges(),  graph_main.get_graph(),n_colors)
            sa_solution.main_loop(max_iterations, min_temp,totaliteration)
            solution = sa_solution.get_best_state()
            print("Best solution:")
            solution.print_chromosome()
            print(f"FIT: {solution.get_fitness()}")

        elif select_method == 3:
            # Tabu Search parameters
            max_iterations = 10000
            neighborhood_size = 5
            n_colors = 0

            if n_graph == 0:
                neighborhood_size = 4
                n_colors = 4

            if n_graph == 1:
                n_colors = 5
            
            if n_graph == 2:
                neighborhood_size = 6
                n_colors = 9

            if n_graph == 3:
                n_colors = 11
            
            if n_graph == 4:
                n_colors = 12

            

            tabu_solution = Tabu( neighborhood_size,graph_main.get_nodes(), graph_main.get_edges(), graph_main.get_graph(),n_colors=n_colors)
            tabu_solution.main_loop(max_iterations,n_colors,totaliteration=totaliteration)

        else:
            print("Sorry, that input is not correct.")
            return

        end_time = time.time()
        total_time = (end_time - start_time) * 1e9  # Convert seconds to nanoseconds

        print(f"\n\nI found the solution in just {total_time} nanoseconds.")
        print(f"and {totaliteration[0]} iterations.")

        # Save the graph
        save_option = input("Would you like to save the graph to a file? (y/n): ")
        if save_option.lower() == 'y':
            output_file = input("Enter the output file name (without extension): ")
            graph_main.save_graph(output_file)

    elif option == 2:
        graph = Graph()
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Répertoire du script principal
        best_solution_path = os.path.join(current_dir, "best_solution.txt")  # Chemin dynamique
        coloring_files = [best_solution_path]
        print("Select a coloring file:")
        for i, filename in enumerate(coloring_files):
            print(f"[{i}] {filename}")
        file_index = int(input("Enter your choice: "))
        coloring_file = coloring_files[file_index]

        # Parse coloring from file
        coloring = read_coloring_from_file(coloring_file)
        print(f"Coloring loaded: {coloring}")

        graph_files = ["myciel3", "myciel4","DSJC125.1","anna","queen9_9"]  # Graphs to choose from
        print("Select a graph file:")
        for i, filename in enumerate(graph_files):
            print(f"[{i}] {filename}")
        graph_index = int(input("Enter your choice: "))
        graph_file = graph_files[graph_index]
    
        # Load the selected graph
        adjacency_list = graph.load_colored_graph(graph_file)
        print(f"Graph loaded: {adjacency_list}")

        conflicts = check_coloring(adjacency_list, coloring)

    elif option == 3:
        graph = Graph()
        modify_graph(graph)  # Call the modify graph function

    elif option == 4 :
          print("FIN")

    else:
        print("Invalid option selected. Exiting.")

if __name__ == "__main__":
    main()
