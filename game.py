import numpy as np
import copy
import time

TIME_LIMIT = 5.0
start_time = None
node_count = 0

def is_connected(board: np.ndarray, player) -> bool:
    height, width = board.shape
    visited = np.zeros(board.shape, dtype="bool")

    # Directions for orthogonal and diagonal movement
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def check_adjacent(r, c):

        visited[r, c] = True
        # Explore all 8 possible directions
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and not visited[nr, nc] and board[nr, nc] == player:
                check_adjacent(nr, nc)


    start_row, start_col = -1, -1
    found_start = False
    for row in range(height):
        for col in range(width):
            if board[row,col] == player:
                start_row, start_col = row, col
                found_start = True
                break

        if found_start:
            break

    check_adjacent(start_row, start_col)

    # Check if all occurrences of the player have been visited
    all_connected = np.array_equal(visited, board == player)
    return all_connected

def get_winner(board: np.ndarray) -> str:
    w_connected = is_connected(board, "W")
    b_connected = is_connected(board, "B")

    winner = "none"
    if w_connected:
        if b_connected:
            winner = "tie"
        else:
            winner = "W"
    elif b_connected:
        winner = "B"

    return winner

def legal_moves(start_row, start_col, board: np.ndarray):
    moves = []

    player = board[start_row, start_col]
    opponent = "W" if player == "B" else "B"

    board_height, board_width = board.shape

    row = board[start_row]
    col = board[:,start_col]

    main_offset = start_col - start_row
    main_diag = board.diagonal(main_offset)
    main_diag_len = len(main_diag)

    rot_row = start_col
    rot_col = board_height - 1 - start_row
    anti_offset = rot_col - rot_row
    anti_diag = np.rot90(board, k=3).diagonal(anti_offset)
    anti_diag_len = len(anti_diag)

    pos_in_main = start_row if start_col >= start_row else start_col
    pos_in_anti = rot_row if rot_col >= rot_row else rot_col

    line_attributes = (
        (row, "row", board_width, start_col),
        (col, "col", board_height, start_row),
        (main_diag, "main_diag", main_diag_len, pos_in_main),
        (anti_diag, "anti_diag", anti_diag_len, pos_in_anti)
    )

    for line, type, length, pos in line_attributes:
        jumps = np.count_nonzero(line != "N")

        for direction in (1,-1):
            dir_step = jumps * direction
            dest = pos + dir_step
            in_bounds = 0 <= dest < length

            if in_bounds and line[dest] != player:
                not_over_opponent = False
                for i in range(pos+direction, dest, direction):
                    if line[i] == opponent:
                        break
                else:
                    not_over_opponent = True

                if not_over_opponent:
                    if type == "row":
                        moves.append((start_row,dest))
                    elif type == "col":
                        moves.append((dest,start_col))
                    elif type == "main_diag":
                        moves.append((start_row+dir_step,start_col+dir_step))
                    elif type == "anti_diag":
                        moves.append((start_row-dir_step,start_col+dir_step))

    return moves

def board_static_evaluation(board: np.ndarray) -> float:
    field_values = np.array([
        [-80, -25, -20, -20, -20, -20, -25, -80],
        [-25,  10,  10,  10,  10,  10,  10, -25],
        [-20,  10,  25,  25,  25,  25,  10, -20],
        [-20,  10,  25,  50,  50,  25,  10, -20],
        [-20,  10,  25,  50,  50,  25,  10, -20],
        [-20,  10,  25,  25,  25,  25,  10, -20],
        [-25,  10,  10,  10,  10,  10,  10, -25],
        [-80, -25, -20, -20, -20, -20, -25, -80]
    ])

    is_white = board == "W"
    is_black = board == "B"

    white_count = np.count_nonzero(is_white)
    black_count = np.count_nonzero(is_black)

    white_score = np.sum(field_values * is_white) / white_count
    black_score = np.sum(field_values * is_black) / black_count

    return white_score - black_score

def is_move_legal(start_row, start_col, dest_row, dest_col, board: np.ndarray) -> bool:
    if (dest_row, dest_col) in legal_moves(start_row, start_col, board):
        return True
    else:
        return False


def computer_move(board, color="W"):
    global start_time, node_count
    start_time = time.time()
    node_count = 0
    board = np.array(board, dtype="U1")
    maximizing = color == "W"

    best_score = -float("inf") if maximizing else float("inf")
    best_move = None
    depth = 1
    reached_depth = 0

    while True:
        if time.time() - start_time >= TIME_LIMIT:
            break

        try:
            score, move = minimax(board, depth, -float("inf"), float("inf"), maximizing)
            if move is not None:
                if (maximizing and score == float("inf")) or (not maximizing and score == float("-inf")):
                    (start_row, start_col), (dest_row, dest_col) = move
                    board[start_row, start_col] = "N"
                    board[dest_row, dest_col] = color
                    elapsed_time = round(time.time() - start_time, 2)
                    return board, elapsed_time, depth, node_count

                if score == best_score:
                    break

                best_score = score
                best_move = move
                reached_depth = depth

        except TimeoutError:
            break

        if time.time() - start_time >= TIME_LIMIT:
            break

        depth += 1

    if best_move is None:
        return board, 0.0, 0, 0

    (start_row, start_col), (dest_row, dest_col) = best_move
    board[start_row, start_col] = "N"
    board[dest_row, dest_col] = color
    elapsed_time = round(time.time() - start_time, 2)
    return board, elapsed_time, reached_depth, node_count

def all_possible_moves(board, player):
    board = np.array(board, dtype="U1")
    moves = []
    for row in range(8):
        for col in range(8):
            if board[row, col] == player:
                for dest_row, dest_col in legal_moves(row, col, board):
                    moves.append(((row, col), (dest_row, dest_col)))
    return moves

def apply_move(board, move):
    board_copy = copy.deepcopy(board)
    (start_row, start_col), (dest_row, dest_col) = move
    board_copy[dest_row, dest_col] = board_copy[start_row, start_col]
    board_copy[start_row, start_col] = "N"
    return board_copy

def minimax(board, depth, alpha, beta, maximizing_player):
    global start_time, node_count
    if time.time() - start_time >= TIME_LIMIT:
        raise TimeoutError()
    
    node_count += 1

    winner = get_winner(board)

    if depth == 0 or winner != "none":
        if winner == "none":
            return (board_static_evaluation(board), None)
        elif winner == "W":
            return (float("inf"), None)
        elif winner == "B":
            return (float("-inf"), None)
        elif winner == "tie":
            return (0, None)

    best_move = None

    if maximizing_player:
        max_eval = -float('inf')
        for move in all_possible_moves(board, "W"):
            new_board = apply_move(board, move)
            eval, _ = minimax(new_board, depth-1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha: #Implementing alpha-beta pruning
                break #Beta cutoff
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in all_possible_moves(board, "B"):
            new_board = apply_move(board, move)
            eval, _ = minimax(new_board, depth-1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha: #Implementing alpha-beta pruning
                break #Alpha cutoff
        return min_eval, best_move
