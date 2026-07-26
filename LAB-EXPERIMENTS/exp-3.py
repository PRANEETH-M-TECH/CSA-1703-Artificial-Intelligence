# Experiment 3: Water Jug Problem
from collections import deque

def water_jug_problem(capacity_a, capacity_b, target):
    # Queue stores tuples of (jug_a, jug_b, path_history)
    queue = deque([(0, 0, [(0, 0)])])
    visited = set([(0, 0)])

    while queue:
        a, b, path = queue.popleft()

        if a == target or b == target:
            return path

        # Possible operations:
        # 1. Fill Jug A
        # 2. Fill Jug B
        # 3. Empty Jug A
        # 4. Empty Jug B
        # 5. Pour A into B
        # 6. Pour B into A
        states = [
            (capacity_a, b),
            (a, capacity_b),
            (0, b),
            (a, 0),
            (a - min(a, capacity_b - b), b + min(a, capacity_b - b)),
            (a + min(b, capacity_a - a), b - min(b, capacity_a - a))
        ]

        for next_a, next_b in states:
            if (next_a, next_b) not in visited:
                visited.add((next_a, next_b))
                queue.append((next_a, next_b, path + [(next_a, next_b)]))

    return None

if __name__ == "__main__":
    print("--- Experiment 3: Water Jug Problem ---")
    cap_a, cap_b, target = 4, 3, 2
    print(f"Jug A Capacity: {cap_a}L, Jug B Capacity: {cap_b}L, Target: {target}L\n")
    
    solution = water_jug_problem(cap_a, cap_b, target)
    if solution:
        print("Steps to reach target:")
        for step, (a, b) in enumerate(solution):
            print(f"Step {step}: Jug A = {a}L, Jug B = {b}L")
    else:
        print("No solution possible.")
