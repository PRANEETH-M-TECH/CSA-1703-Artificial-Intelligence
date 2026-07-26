# Experiment 14: Alpha-Beta Pruning

def alpha_beta_minimax(depth, node_index, is_max, scores, alpha, beta, height):
    # Base case: leaf node
    if depth == height:
        return scores[node_index]

    if is_max:
        best = float('-inf')
        for i in range(2):
            val = alpha_beta_minimax(depth + 1, node_index * 2 + i, False, scores, alpha, beta, height)
            best = max(best, val)
            alpha = max(alpha, best)
            
            # Beta Cutoff (Pruning)
            if beta <= alpha:
                print(f"Pruned branch at depth {depth}, node_index {node_index}")
                break
        return best
    else:
        best = float('inf')
        for i in range(2):
            val = alpha_beta_minimax(depth + 1, node_index * 2 + i, True, scores, alpha, beta, height)
            best = min(best, val)
            beta = min(beta, best)
            
            # Alpha Cutoff (Pruning)
            if beta <= alpha:
                print(f"Pruned branch at depth {depth}, node_index {node_index}")
                break
        return best

if __name__ == "__main__":
    print("--- Experiment 14: Alpha-Beta Pruning ---")
    scores = [3, 5, 6, 9, 1, 2, 0, -1]
    import math
    tree_height = int(math.log2(len(scores)))
    
    alpha_init = float('-inf')
    beta_init = float('inf')
    
    optimal_value = alpha_beta_minimax(0, 0, True, scores, alpha_init, beta_init, tree_height)
    print(f"\nLeaf values: {scores}")
    print(f"Optimal Value evaluated with Alpha-Beta Pruning: {optimal_value}")
