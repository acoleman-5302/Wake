import random
import time
import numpy as np

# Board dimensions
N = 6  # Change this for different sizes

# Possible moves for a knight
MOVES = [(-2, -1), (-1, -2), (1, -2), (2, -1),
         (2, 1), (1, 2), (-1, 2), (-2, 1)]

def torus_coord(x, N):
    """Wrap around the board edges to simulate a torus"""
    return x % N

def get_valid_moves(board, x, y):
    """Get all valid moves from (x, y) on a toroidal board"""
    moves = []
    for dx, dy in MOVES:
        nx, ny = torus_coord(x + dx, N), torus_coord(y + dy, N)
        if board[nx, ny] == 0:
            moves.append((nx, ny))
    return moves

def warnsdorff_next_move(board, x, y):
    """Choose the next move using Warnsdorff's heuristic"""
    valid_moves = get_valid_moves(board, x, y)
    if not valid_moves:
        return None
    
    # Rank moves by least onward moves
    ranked_moves = sorted(valid_moves, key=lambda move: len(get_valid_moves(board, move[0], move[1])))
    return ranked_moves[0]

def print_board(board):
    """Print the current state of the board"""
    symbols = {0: '·', 1: 'A', 2: 'B'}
    print("  " + " ".join(str(j) for j in range(N)))
    print("  " + "---" * N)
    for i in range(N):
        print(str(i) + "| " + " ".join(symbols[board[i, j]] for j in range(N)))
    print()

def knights_game():
    """Two knights (A and B) attempt a knight's tour on an N by N toroidal board using Warnsdorff's rule."""
    board = np.zeros((N, N), dtype=int)
    knight_a_pos = (0, 0)
    knight_b_pos = (N - 1, N - 1)
    board[knight_a_pos] = 1
    board[knight_b_pos] = 2
    
    current_knight = 1  # 1 for Knight A, 2 for Knight B
    moves_made = 2
    total_squares = N * N
    
    print("Game Start!")
    print_board(board)
    
    no_move_counter = 0
    while moves_made < total_squares and no_move_counter < 2:
        knight_name = "A" if current_knight == 1 else "B"
        current_pos = knight_a_pos if current_knight == 1 else knight_b_pos
        
        print(f"Knight {knight_name}'s turn. Current position: {current_pos}")
        next_move = warnsdorff_next_move(board, current_pos[0], current_pos[1])
        
        if not next_move:
            print(f"Knight {knight_name} has no valid moves. Turn skipped.")
            no_move_counter += 1
        else:
            no_move_counter = 0
            new_x, new_y = next_move
            board[new_x, new_y] = current_knight
            moves_made += 1
            print(f"Knight {knight_name} moves to ({new_x}, {new_y})")
            
            if current_knight == 1:
                knight_a_pos = (new_x, new_y)
            else:
                knight_b_pos = (new_x, new_y)
            
            print_board(board)
        
        current_knight = 3 - current_knight  # Switch turns
        time.sleep(0.5)
    
    print("Game over!")
    print_board(board)
    print(f"Total moves made: {moves_made} out of {total_squares}")

# Run the game
knights_game()
