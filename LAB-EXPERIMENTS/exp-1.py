# Experiment 1: 8-Puzzle Problem using Breadth-First Search (BFS)
from collections import deque

def solve_8_puzzle(initial_state):
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    
    # Directions: Up, Down, Left, Right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    queue = deque([(initial_state, [])])
    visited = {initial_state}
    
    while queue:
        state, path = queue.popleft()
        
        if state == goal_state:
            return path + [state]
            
        zero_index = state.index(0)
        r, c = zero_index // 3, zero_index % 3
        
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_zero = nr * 3 + nc
                state_list = list(state)
                # Swap empty tile (0) with target tile
                state_list[zero_index], state_list[new_zero] = state_list[new_zero], state_list[zero_index]
                new_state = tuple(state_list)
                
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [state]))
                    
    return None

def print_board(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

if __name__ == "__main__":
    print("--- Experiment 1: 8-Puzzle Problem ---")
    start = (1, 2, 3, 4, 0, 6, 7, 5, 8)
    print("Initial State:")
    print_board(start)
    
    solution = solve_8_puzzle(start)
    if solution:
        print(f"Solved in {len(solution)-1} steps:")
        for step in solution:
            print_board(step)
    else:
        print("No solution found.")
