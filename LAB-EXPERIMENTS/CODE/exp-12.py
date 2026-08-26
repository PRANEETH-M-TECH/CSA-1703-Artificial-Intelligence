# Experiment 12: Tic-Tac-Toe Game

def print_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def is_board_full(board):
    return ' ' not in board

def play_game_simulation():
    board = [' '] * 9
    players = ['X', 'O']
    # Simulated moves sequence
    simulated_moves = [0, 4, 1, 3, 2] # Player 'X' wins on top row (0, 1, 2)
    
    print("Simulating a sample Tic-Tac-Toe game...")
    turn = 0
    
    for move in simulated_moves:
        current_player = players[turn % 2]
        board[move] = current_player
        print(f"Player {current_player} places at position {move+1}:")
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player '{current_player}' WINS the game!")
            return
            
        if is_board_full(board):
            print("It's a DRAW!")
            return
            
        turn += 1

if __name__ == "__main__":
    print("--- Experiment 12: Tic-Tac-Toe Game ---")
    play_game_simulation()
