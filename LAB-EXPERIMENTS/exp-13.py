# Experiment 13: Minimax Algorithm in Game Theory
import math

def minimax(depth, node_index, is_max, scores, height):
    # Base case: leaf node reached
    if depth == height:
        return scores[node_index]

    if is_max:
        return max(
            minimax(depth + 1, node_index * 2, False, scores, height),
            minimax(depth + 1, node_index * 2 + 1, False, scores, height)
        )
    else:
        return min(
            minimax(depth + 1, node_index * 2, True, scores, height),
            minimax(depth + 1, node_index * 2 + 1, True, scores, height)
        )

if __name__ == "__main__":
    print("--- Experiment 13: Minimax Algorithm ---")
    # Leaf node values (scores)
    scores = [3, 5, 2, 9, 12, 5, 23, 23]
    tree_height = int(math.log2(len(scores)))

    optimal_val = minimax(0, 0, True, scores, tree_height)
    print(f"Leaf Scores: {scores}")
    print(f"Optimal Value evaluated by Minimax: {optimal_val}")
