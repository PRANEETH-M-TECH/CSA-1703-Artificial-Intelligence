# Experiment 7: Breadth-First Search (BFS)
from collections import deque

def bfs(graph, start_node):
    visited = set()
    queue = deque([start_node])
    visited.add(start_node)
    
    traversal_order = []

    while queue:
        node = queue.popleft()
        traversal_order.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return traversal_order

if __name__ == "__main__":
    print("--- Experiment 7: Breadth-First Search (BFS) ---")
    # Sample Graph represented as adjacency list
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }
    
    start = 'A'
    result = bfs(graph, start)
    print(f"Graph Adjacency List: {graph}")
    print(f"BFS Traversal starting from '{start}': {' -> '.join(result)}")
