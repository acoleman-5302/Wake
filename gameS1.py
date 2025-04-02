import numpy as np
import random
import time

# Board dimensions
N = 4  # Change this for different sizes

# Possible moves for a knight
MOVES = [(-2, -1), (-1, -2), (1, -2), (2, -1),
         (2, 1), (1, 2), (-1, 2), (-2, 1)]


def is_torus_move(x, y, nx, ny, N):
    """Check if a move requires wrapping around the board (torus move)"""
    # If the new coordinates differ by more than the added move, we must have wrapped
    if abs((nx - x) % N) != abs(nx - x) or abs((ny - y) % N) != abs(ny - y):
        return True
    return False


def torus_coord(x, N):
    """Wrap around the board edges to simulate a torus"""
    return x % N


def get_valid_moves(board, x, y):
    """Get all valid moves from (x, y) on a toroidal board"""
    moves = []
    for dx, dy in MOVES:
        nx, ny = torus_coord(x + dx, N), torus_coord(y + dy, N)
        if board[nx, ny] == 0:  # Check if the square is unvisited
            torus_flag = ((x + dx) != nx or (y + dy) != ny)  # if wrapping occurred
            moves.append((nx, ny, torus_flag))
    return moves


def print_board(board):
    """Print the current state of the board"""
    symbols = {0: '·', 1: 'A', 2: 'B'}

    # Print column headers
    print("  ", end="")
    for j in range(N):
        print(" " + str(j) + " ", end="")
    print("\
  " + "---" * N)

    # Print rows with row headers
    for i in range(N):
        print(str(i) + "|", end="")
        for j in range(N):
            print(" " + symbols[board[i, j]] + " ", end="")
        print()
    print()


def knights_game():
    """
    Two knights (A and B) attempt a knight's tour on an N by N toroidal board.
    - If a knight's turn has no valid moves, that turn is skipped.
    - If the knight's first move is non-toroidal (grid-only move), it gets a second move.
    - If the move requires wrapping (torus move), its turn ends immediately.
    - The game ends when either the board is filled (win) or when both knights consecutively have no valid moves (tie).
    """
    board = np.zeros((N, N), dtype=int)

    # Starting positions
    knight_a_pos = (0, 0)
    knight_b_pos = (N - 1, N - 1)
    board[knight_a_pos] = 1
    board[knight_b_pos] = 2

    current_knight = 1  # 1 for Knight A, 2 for Knight B
    moves_made = 2
    total_squares = N * N

    print("Game Start!")
    print("Knight A starts at position (0, 0)")
    print("Knight B starts at position (" + str(N - 1) + ", " + str(N - 1) + ")")
    print_board(board)

    # Track consecutive no-move turns
    no_move_counter = 0

    while moves_made < total_squares and no_move_counter < 2:
        knight_name = "A" if current_knight == 1 else "B"
        current_pos = knight_a_pos if current_knight == 1 else knight_b_pos

        print("Knight " + knight_name + "'s turn. Current position: " + str(current_pos))
        valid_moves = get_valid_moves(board, current_pos[0], current_pos[1])

        if not valid_moves:
            print("Knight " + knight_name + " has no valid moves. Turn skipped.")
            no_move_counter += 1
        else:
            no_move_counter = 0  # reset counter if a move is available
            # First move
            next_move = random.choice(valid_moves)
            new_x, new_y, is_torus_flag = next_move
            board[new_x, new_y] = current_knight
            moves_made += 1
            print("Knight " + knight_name + " moves to (" + str(new_x) + ", " + str(new_y) + ")")
            if is_torus_flag:
                print("This was a torus move. Knight " + knight_name + "'s turn ends.")

            # Update position
            if current_knight == 1:
                knight_a_pos = (new_x, new_y)
            else:
                knight_b_pos = (new_x, new_y)

            print_board(board)

            # Second move if first move was not a torus move
            if not is_torus_flag:
                second_moves = get_valid_moves(board, new_x, new_y)
                if second_moves:
                    print("Knight " + knight_name + " gets a second move!")
                    next_move2 = random.choice(second_moves)
                    new_x2, new_y2, _ = next_move2
                    board[new_x2, new_y2] = current_knight
                    moves_made += 1
                    print("Knight " + knight_name + " moves to (" + str(new_x2) + ", " + str(
                        new_y2) + ") for second move")
                    if current_knight == 1:
                        knight_a_pos = (new_x2, new_y2)
                    else:
                        knight_b_pos = (new_x2, new_y2)
                    print_board(board)
                else:
                    print("Knight " + knight_name + " has no valid second moves.")

        # Switch knight turn
        current_knight = 3 - current_knight  # toggles between 1 and 2
        time.sleep(0.5)

    # End of game
    if moves_made == total_squares:
        last_knight = "A" if current_knight == 2 else "B"
        print("Game over! Knight " + last_knight + " wins by completing the board!")
    else:
        print("Game over! It's a tie - the board cannot be completed.")

    print("Final board state:")
    print_board(board)
    print("Total moves made: " + str(moves_made) + " out of " + str(total_squares) + " squares")


# Run the game
knights_game()