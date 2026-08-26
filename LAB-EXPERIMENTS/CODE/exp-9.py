# Experiment 9: Travelling Salesman Problem (TSP) using Brute Force
import itertools

def solve_tsp(graph, start_city):
    cities = list(graph.keys())
    cities.remove(start_city)
    
    min_cost = float('inf')
    best_path = []
    
    for perm in itertools.permutations(cities):
        current_path = [start_city] + list(perm) + [start_city]
        current_cost = 0
        valid_path = True
        
        for i in range(len(current_path) - 1):
            u, v = current_path[i], current_path[i+1]
            if v in graph[u]:
                current_cost += graph[u][v]
            else:
                valid_path = False
                break
                
        if valid_path and current_cost < min_cost:
            min_cost = current_cost
            best_path = current_path
            
    return best_path, min_cost

if __name__ == "__main__":
    print("--- Experiment 9: Travelling Salesman Problem (TSP) ---")
    # Distance Matrix / Adjacency Graph
    graph = {
        'A': {'B': 10, 'C': 15, 'D': 20},
        'B': {'A': 10, 'C': 35, 'D': 25},
        'C': {'A': 15, 'B': 35, 'D': 30},
        'D': {'A': 20, 'B': 25, 'C': 30}
    }
    
    start = 'A'
    best_path, min_cost = solve_tsp(graph, start)
    print(f"Cities distance graph: {graph}\n")
    print(f"Optimal Path starting from '{start}': {' -> '.join(best_path)}")
    print(f"Minimum Tour Distance: {min_cost}")
