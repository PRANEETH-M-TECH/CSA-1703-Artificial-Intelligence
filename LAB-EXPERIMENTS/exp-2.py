# Experiment 2: 8-Queen Problem using Backtracking

N = 8

def is_safe(board, row, col):
    # Check column on upper side
    for i in range(row):
        if board[i] == col:
            return False
            
    # Check upper left diagonal
    for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
        if board[i] == j:
            return False
            
    # Check upper right diagonal
    for i, j in zip(range(row - 1, -1, -1), range(col + 1, N)):
        if board[i] == j:
            return False
            
    return True

def solve_n_queens(board, row):
    if row >= N:
        return True

    for col in range(N):
        if is_safe(board, row, col):
            board[row] = col
            if solve_n_queens(board, row + 1):
                return True
            board[row] = -1 # Backtrack

    return False

def print_solution(board):
    for i in range(N):
        row_str = ""
        for j in range(N):
            if board[i] == j:
                row_str += " Q "
            else:
                row_str += " . "
        print(row_str)

if __name__ == "__main__":
    print("--- Experiment 2: 8-Queen Problem ---")
    board = [-1] * N
    if solve_n_queens(board, 0):
        print("One valid solution for 8-Queens:")
        print_solution(board)
    else:
        print("No solution exists.")
