import numpy as np
import random

# Board dimensions
N = 4  # Change this for different sizes

# Possible moves for a knight
MOVES = [(-2, -1), (-1, -2), (1, -2), (2, -1),
         (2, 1), (1, 2), (-1, 2), (-2, 1)]

def torus_coord(x, N):
    """ Wrap around the board edges to simulate a torus """
    return x % N

def get_valid_moves(board, x, y):
    """ Get all valid moves from (x, y) on a toroidal board """
    moves = []
    for dx, dy in MOVES:
        nx, ny = torus_coord(x + dx, N), torus_coord(y + dy, N)
        if board[nx, ny] == -1:  # Check if the square is unvisited
            moves.append((nx, ny))
    return moves

def knights_tour_torus(x=0, y=0):
    """ Solves the knight's tour problem on a toroidal board """
    board = np.full((N, N), -1)
    board[x, y] = 1  # Start position
    
    for move_num in range(1, N * N):
        moves = get_valid_moves(board, x, y)
        if not moves:
            return None  # No solution found

        # Use Warnsdorff’s heuristic (sort by least available moves)
        moves.sort(key=lambda pos: len(get_valid_moves(board, pos[0], pos[1])))

        x, y = moves[0]
        board[x, y] = move_num +1 # Mark move on board

    return board

# Run the solver
solution = knights_tour_torus()
if solution is not None:
    print("Knight's Tour on a Toroidal Chessboard:")
    print(solution)
else:
    print("No solution found.")
