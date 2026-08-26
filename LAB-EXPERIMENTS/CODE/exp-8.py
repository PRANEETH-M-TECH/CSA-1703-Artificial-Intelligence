# Experiment 8: Depth-First Search (DFS)

def dfs(graph, node, visited=None, traversal_order=None):
    if visited is None:
        visited = set()
    if traversal_order is None:
        traversal_order = []

    visited.add(node)
    traversal_order.append(node)

    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited, traversal_order)

    return traversal_order

if __name__ == "__main__":
    print("--- Experiment 8: Depth-First Search (DFS) ---")
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
    result = dfs(graph, start)
    print(f"Graph Adjacency List: {graph}")
    print(f"DFS Traversal starting from '{start}': {' -> '.join(result)}")
