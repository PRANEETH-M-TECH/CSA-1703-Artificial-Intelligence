"""
Water Jug Problem using Breadth-First Search (BFS)
CSA-1703, Unit-1, Assessment-1
"""

from collections import deque

class WaterJugSolver:
    def __init__(self, capacity_x, capacity_y, target_amount):
        self.capacity_x = capacity_x
        self.capacity_y = capacity_y
        self.target = target_amount
        
    def get_neighbors(self, state):
        """Generate all possible next states from current state"""
        x, y = state
        neighbors = []
        
        # 1. Fill jug X
        neighbors.append((self.capacity_x, y))
        
        # 2. Fill jug Y
        neighbors.append((x, self.capacity_y))
        
        # 3. Empty jug X
        neighbors.append((0, y))
        
        # 4. Empty jug Y
        neighbors.append((x, 0))
        
        # 5. Pour X to Y
        pour_xy = min(x, self.capacity_y - y)
        neighbors.append((x - pour_xy, y + pour_xy))
        
        # 6. Pour Y to X
        pour_yx = min(y, self.capacity_x - x)
        neighbors.append((x + pour_yx, y - pour_yx))
        
        return neighbors
    
    def solve(self):
        """Solve using BFS"""
        initial_state = (0, 0)
        queue = deque([(initial_state, [initial_state])])
        visited = {initial_state}
        
        while queue:
            current_state, path = queue.popleft()
            x, y = current_state
            
            # Check if target reached
            if x == self.target or y == self.target:
                return path, len(path) - 1
            
            # Explore neighbors
            for neighbor in self.get_neighbors(current_state):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        return None, -1

# Problem instance
solver = WaterJugSolver(capacity_x=4, capacity_y=3, target_amount=2)
solution_path, steps = solver.solve()

# Display results
if solution_path:
    print("=== Solution Found ===")
    print(f"Steps required: {steps}")
    print("Path:")
    for i, (x, y) in enumerate(solution_path):
        print(f"Step {i}: ({x}, {y})")
else:
    print("No solution found")





#Question-2: Mars Rover PEAS (Utility Agent)

class MarsRoverUtilityAgent:
    def __init__(self):
        self.battery = 100
        self.samples_collected = 0
        self.location = (0, 0)
        self.state = 'IDLE'

    def percept(self, sensor_data):
        self.terrain = sensor_data.get('terrain')
        self.obstacle = sensor_data.get('obstacle_ahead')
        self.sunlight = sensor_data.get('sunlight_level')

    def calculate_utility(self, action):
        # Simplistic utility function evaluating trade-offs
        if action == "COLLECT" and self.terrain == "high_value":
            return 100 - (100 - self.battery) * 0.5 
        elif action == "MOVE_FORWARD" and not self.obstacle:
            return 50
        elif action == "RECHARGE" and self.sunlight == "high":
            return 80 if self.battery < 40 else 10
        return -1 # Invalid or risky action

    def act(self):
        actions = ["MOVE_FORWARD", "TURN", "COLLECT", "RECHARGE"]
        best_action = max(actions, key=lambda a: self.calculate_utility(a))
        
        if best_action == "COLLECT":
            self.samples_collected += 1
            self.battery -= 10
            return "Collecting scientific sample..."
        elif best_action == "MOVE_FORWARD":
            self.battery -= 2
            return "Moving forward safely."
        elif best_action == "RECHARGE":
            self.battery = min(100, self.battery + 20)
            return "Recharging solar panels."
        else:
            return "Turning to avoid obstacle."

rover = MarsRoverUtilityAgent()
rover.percept({'terrain': 'high_value', 'obstacle_ahead': False, 'sunlight_level': 'high'})
print(f"Rover Decision: {rover.act()}")
print(f"Battery Level: {rover.battery}%, Samples: {rover.samples_collected}")


# Question-3: 8-Puzzle Problem (A* Search)
"""
8-Puzzle Problem using A* Search Algorithm
CSA-1703, Unit-1, Assessment-1
"""

class EightPuzzleSolver:
    def __init__(self, initial_state, goal_state):
        self.initial_state = tuple(tuple(row) for row in initial_state)
        self.goal_state = tuple(tuple(row) for row in goal_state)
    
    def manhattan_distance(self, state):
        """Calculate Manhattan distance heuristic"""
        distance = 0
        for r in range(3):
            for c in range(3):
                val = state[r][c]
                if val != 0:
                    goal_r, goal_c = divmod(val - 1, 3)
                    distance += abs(r - goal_r) + abs(c - goal_c)
        return distance
    
    def get_neighbors(self, state):
        """Get all valid next states"""
        neighbors = []
        zero_r, zero_c = -1, -1
        
        # Find empty tile
        for r in range(3):
            for c in range(3):
                if state[r][c] == 0:
                    zero_r, zero_c = r, c
                    break
        
        # Possible moves: up, down, left, right
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dr, dc in moves:
            nr, nc = zero_r + dr, zero_c + dc
            
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_state_list = [list(row) for row in state]
                # Swap empty tile with neighbor
                new_state_list[zero_r][zero_c] = new_state_list[nr][nc]
                new_state_list[nr][nc] = 0
                neighbors.append(tuple(tuple(row) for row in new_state_list))
        
        return neighbors
    
    def solve(self):
        """Solve using A* search with Manhattan distance heuristic"""
        # Priority queue: (f_score, g_score, state, path)
        # f_score = g_score + h_score
        priority_queue = []
        
        # Open set: {state: g_score}
        open_set = {self.initial_state: 0}
        
        # Path tracking
        path_tracker = {self.initial_state: []}
        
        g_score = 0
        h_score = self.manhattan_distance(self.initial_state)
        f_score = g_score + h_score
        
        priority_queue.append((f_score, g_score, self.initial_state, []))
        
        while priority_queue:
            # Get state with lowest f_score
            priority_queue.sort()
            f, g, current_state, path = priority_queue.pop(0)
            
            # Goal check
            if current_state == self.goal_state:
                return path + [current_state], len(path)
            
            # Explore neighbors
            for neighbor in self.get_neighbors(current_state):
                new_g_score = g + 1
                
                if neighbor not in open_set or new_g_score < open_set[neighbor]:
                    open_set[neighbor] = new_g_score
                    new_h_score = self.manhattan_distance(neighbor)
                    new_f_score = new_g_score + new_h_score
                    
                    # Update priority queue
                    if neighbor in open_set and [f, g, current_state, path] in priority_queue:
                        priority_queue.remove([f, g, current_state, path])
                    
                    priority_queue.append((new_f_score, new_g_score, neighbor, path + [current_state]))
                    path_tracker[neighbor] = path + [current_state]
        
        return None, -1

# Problem instance
initial_state = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 5, 8]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

solver = EightPuzzleSolver(initial_state, goal_state)
solution_path, steps = solver.solve()

# Display results
if solution_path:
    print("=== Solution Found ===")
    print(f"Steps required: {steps}")
    print("Path:")
    for i, state in enumerate(solution_path):
        print(f"\nStep {i}:")
        for row in state:
            print(row)
else:
    print("No solution found")  



#Question-4: OLA Cab Booking (A* Search)
import heapq

def ola_route_finder(graph, start, destination):
    # frontier stores tuples of (estimated_total_cost, current_cost, node, path)
    frontier = [(0, 0, start, [])]
    visited_costs = {start: 0}
    
    # Simple heuristic function (e.g., straight-line distance, mocked as 0 for Dijkstra)
    def heuristic(node, goal):
        return 0 # Converts A* back to Dijkstra's if no coordinates exist

    while frontier:
        est_total, current_cost, current_node, path = heapq.heappop(frontier)
        
        # Update path
        path = path + [current_node]
        
        if current_node == destination:
            return path, current_cost
            
        for neighbor, travel_cost in graph.get(current_node, {}).items():
            new_cost = current_cost + travel_cost
            
            if neighbor not in visited_costs or new_cost < visited_costs[neighbor]:
                visited_costs[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, destination)
                heapq.heappush(frontier, (priority, new_cost, neighbor, path))
                
    return None, float('inf')

# Mock OLA City Graph
city_map = {
    'Pickup': {'Junction A': 5, 'Junction B': 2},
    'Junction A': {'Destination': 4},
    'Junction B': {'Junction A': 1, 'Destination': 7},
    'Destination': {}
}

route, cost = ola_route_finder(city_map, 'Pickup', 'Destination')
print(f"Optimal OLA Cab Route: {' -> '.join(route)}")
print(f"Total Trip Cost/Time: {cost} mins")




#Question-5: Logistics Company (Uniform Cost Search):

import heapq

def uniform_cost_search(graph, start, goal):
    # Priority Queue stores tuples of (cumulative_cost, current_node, path)
    priority_queue = [(0, start, [])]
    visited = set()

    while priority_queue:
        cost, node, path = heapq.heappop(priority_queue)
        
        if node in visited:
            continue
            
        visited.add(node)
        path = path + [node]

        if node == goal:
            return path, cost

        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(priority_queue, (cost + weight, neighbor, path))
                
    return None, float('inf')

# Graph representation as adjacency list based on the provided figure
delivery_network = {
    'S': [('A', 1), ('G', 12)],
    'A': [('B', 3), ('C', 1)],
    'B': [('D', 3)],
    'C': [('D', 1), ('G', 2)],
    'D': [('G', 3)],
    'G': []git 
}

optimal_path, optimal_cost = uniform_cost_search(delivery_network, 'S', 'G')
print(f"Least-cost path from S to G: {' -> '.join(optimal_path)}")
print(f"Total delivery cost: {optimal_cost}")


