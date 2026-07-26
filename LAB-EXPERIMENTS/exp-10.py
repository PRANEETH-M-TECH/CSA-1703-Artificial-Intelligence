# Experiment 10: A* Algorithm
import heapq

def a_star_search(graph, heuristics, start, goal):
    # Priority Queue stores tuples of (f_score, g_score, current_node, path)
    open_list = [(heuristics[start], 0, start, [start])]
    visited = set()

    while open_list:
        f, g, current, path = heapq.heappop(open_list)

        if current == goal:
            return path, g

        if current in visited:
            continue
        visited.add(current)

        for neighbor, cost in graph.get(current, {}).items():
            if neighbor not in visited:
                g_new = g + cost
                f_new = g_new + heuristics.get(neighbor, 0)
                heapq.heappush(open_list, (f_new, g_new, neighbor, path + [neighbor]))

    return None, float('inf')

if __name__ == "__main__":
    print("--- Experiment 10: A* Search Algorithm ---")
    
    # Graph representation with path costs
    graph = {
        'A': {'B': 6, 'F': 3},
        'B': {'C': 3, 'D': 2},
        'C': {'D': 1, 'E': 5},
        'D': {'E': 8},
        'E': {'I': 5, 'J': 5},
        'F': {'G': 1, 'H': 7},
        'G': {'I': 3},
        'H': {'I': 2},
        'I': {'E': 5, 'J': 3},
        'J': {}
    }

    # Heuristic estimate h(n) to Goal 'J'
    heuristics = {
        'A': 10, 'B': 8, 'C': 5, 'D': 7,
        'E': 3, 'F': 6, 'G': 5, 'H': 3,
        'I': 1, 'J': 0
    }

    start_node, goal_node = 'A', 'J'
    path, cost = a_star_search(graph, heuristics, start_node, goal_node)
    
    if path:
        print(f"Optimal Path from '{start_node}' to '{goal_node}': {' -> '.join(path)}")
        print(f"Total Path Cost: {cost}")
    else:
        print("No path found.")
