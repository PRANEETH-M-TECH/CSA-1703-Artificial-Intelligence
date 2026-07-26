# Experiment 5: Missionaries and Cannibals Problem
from collections import deque

# State representation: (M_left, C_left, boat_position)
# boat_position: 1 for Left bank, 0 for Right bank

def is_valid_state(m, c):
    # Total missionaries and cannibals is 3 each
    if m < 0 or m > 3 or c < 0 or c > 3:
        return False
    # Check left bank: Missionaries cannot be outnumbered by Cannibals if M > 0
    if m > 0 and m < c:
        return False
    # Check right bank: (3-m) missionaries, (3-c) cannibals
    m_right, c_right = 3 - m, 3 - c
    if m_right > 0 and m_right < c_right:
        return False
    return True

def solve_missionaries_cannibals():
    start_state = (3, 3, 1)
    goal_state = (0, 0, 0)
    
    # Possible boat moves: (M, C)
    moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    
    queue = deque([(start_state, [start_state])])
    visited = {start_state}
    
    while queue:
        (m, c, boat), path = queue.popleft()
        
        if (m, c, boat) == goal_state:
            return path
            
        for dm, dc in moves:
            if boat == 1: # Moving from Left to Right
                new_m, new_c, new_boat = m - dm, c - dc, 0
            else: # Moving from Right to Left
                new_m, new_c, new_boat = m + dm, c + dc, 1
                
            if is_valid_state(new_m, new_c):
                new_state = (new_m, new_c, new_boat)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [new_state]))
                    
    return None

if __name__ == "__main__":
    print("--- Experiment 5: Missionaries and Cannibals Problem ---")
    solution = solve_missionaries_cannibals()
    
    if solution:
        print("Sequence of states (M_left, C_left, Boat_Left):")
        for step, (m, c, boat) in enumerate(solution):
            b_str = "Left Bank" if boat == 1 else "Right Bank"
            print(f"Step {step}: Left(M:{m}, C:{c}) | Boat at {b_str} | Right(M:{3-m}, C:{3-c})")
    else:
        print("No solution found.")
