import numpy as np
import copy


def legal_moves(start_row, start_col, board: np.ndarray):
    moves = []

    player = board[start_row, start_col]
    opponent = "W" if player == "B" else "B"

    board_height = board.shape[0]
    board_width = board.shape[1]

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

    pos_in_main = -1
    if main_offset >= 0:
        pos_in_main = start_row
    elif main_offset < 0:
        pos_in_main = start_col

    pos_in_anti = -1
    if anti_offset >= 0:
        pos_in_anti = rot_row
    elif anti_offset < 0:
        pos_in_anti = rot_col

    line_attributes = (
        (row, "row", board_width, start_col),
        (col, "col", board_height, start_row),
        (main_diag, "main_diag", main_diag_len, pos_in_main),
        (anti_diag, "anti_diag", anti_diag_len, pos_in_anti)
    )

    for line, type, length, pos in line_attributes:
        jumps = np.count_nonzero(line != "N")

        forward = pos + jumps
        in_bounds = forward < length

        if in_bounds:
            not_on_ally = line[forward] != player
            if not_on_ally:
                not_over_opponent = False
                for i in range(pos+1, forward):
                    if line[i] == opponent:
                        break
                else:
                    not_over_opponent = True

                if not_over_opponent:
                    if type == "row":
                        moves.append((start_row,forward))
                    elif type == "col":
                        moves.append((forward,start_col))
                    elif type == "main_diag":
                        moves.append((start_row+jumps,start_col+jumps))
                    elif type == "anti_diag":
                        moves.append((start_row-jumps,start_col+jumps))

        backwards = pos - jumps
        in_bounds = backwards >= 0

        if in_bounds:
            not_on_ally = line[backwards] != player
            if not_on_ally:
                not_over_opponent = False
                for i in range(pos-1, backwards, -1):
                    if line[i] == opponent:
                        break
                else:
                    not_over_opponent = True

                if not_over_opponent:
                    if type == "row":
                        moves.append((start_row,backwards))
                    elif type == "col":
                        moves.append((backwards,start_col))
                    elif type == "main_diag":
                        moves.append((start_row-jumps,start_col-jumps))
                    elif type == "anti_diag":
                        moves.append((start_row+jumps,start_col-jumps))
    return moves

def board_static_evaluation(board: np.ndarray) -> int:
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

def is_move_legal(start_row, start_col, dest_row, dest_col, board) -> bool:
    board = np.array(board, dtype="U1")

    if (dest_row, dest_col) in legal_moves(start_row, start_col, board):
        return True
    else:
        return False

# def computer_move(board) -> np.ndarray:

#     board = np.array(board, dtype="U1")
#     piece_coordinates = []

#     for row_index, row in enumerate(board):
#         for col_index, field in enumerate(row):
#             if board[row_index, col_index] == 'W':
#                 piece_coordinates.append((row_index, col_index))

#     moves = []
#     for row_index, col_index in piece_coordinates:
#         dest = legal_moves(row_index, col_index, board)

#         moves.append((row_index, col_index, dest))

#     best_move = moves[0]

#     board[best_move[0],best_move[1]] = "N"
#     board[best_move[2][0][0],best_move[2][0][1]] = "W"

#     return board

def computer_move(board):
    board = np.array(board, dtype="U1")
    score, best_move = minimax(board, depth=3, alpha=-float('inf'), beta=float('inf'), maximizing_player=True)

    if best_move is None:
        return board

    (start_row, start_col), (dest_row, dest_col) = best_move
    board[start_row, start_col] = "N"
    board[dest_row, dest_col] = "W"
    return board

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

def evaluate_board(board):
    # Midlertidig: Oliver skal erstatte dette med heuristik, eller bare brug whatever han kalder sin.
    return board_static_evaluation(board)

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or game_over(board):
        return evaluate_board(board), None

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

def game_over(board):
    #Dummy version, vi skal lave et regelsæt ift gameover
    white_pieces = np.sum(board == "W")
    black_pieces = np.sum(board == "B")
    return white_pieces == 0 or black_pieces == 0
