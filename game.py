import numpy as np
import copy


def legal_moves(start_row, start_col, board: np.ndarray):
    fields = []
    board_height = board.shape[0]
    board_width = board.shape[1]

    row = board[start_row]
    col = board[:,start_col]

    diag_lower_left = board[start_row:,start_col::-1].diagonal()
    diag_upper_right = board[start_row::-1,start_col:].diagonal()
    diag1 = np.concatenate((diag_lower_left[1:], diag_upper_right))

    diag_lower_right = board[start_row:,start_col:].diagonal()
    diag_upper_left = board[start_row::-1,start_col::-1].diagonal()
    diag2 = np.concatenate((diag_lower_right[1:], diag_upper_left))


    pieces_in_row = 0
    for i in row:
        if i != 'N':
            pieces_in_row += 1

    new_col = start_col + pieces_in_row
    if new_col >= 0 and new_col < board_width:
        fields.append((start_row, new_col))

    new_col = start_col - pieces_in_row
    if new_col >= 0 and new_col < board_width:
        fields.append((start_row, new_col))

    pieces_in_col = 0
    for i in col:
        if i != 'N':
            pieces_in_col += 1

    new_row = start_row + pieces_in_col
    if new_row >= 0 and new_row < board_height:
        fields.append((new_row, start_col))

    new_row = start_row - pieces_in_col
    if new_row >= 0 and new_row < board_height:
        fields.append((new_row, start_col))

    pieces_in_diag1 = 0
    for i in diag1:
        if i != 'N':
            pieces_in_diag1 += 1

    new_row = start_row - pieces_in_diag1
    new_col = start_col + pieces_in_diag1
    if new_row >= 0 and new_row < board_height and new_col >= 0 and new_col < board_width:
        fields.append((new_row, new_col))

    new_row = start_row + pieces_in_diag1
    new_col = start_col - pieces_in_diag1
    if new_row >= 0 and new_row < board_height and new_col >= 0 and new_col < board_width:
        fields.append((new_row, new_col))

    pieces_in_diag2 = 0
    for i in diag2:
        if i != 'N':
            pieces_in_diag2 += 1

    new_row = start_row - pieces_in_diag2
    new_col = start_col - pieces_in_diag2
    if new_row >= 0 and new_row < board_height and new_col >= 0 and new_col < board_width:
        fields.append((new_row, new_col))

    new_row = start_row + pieces_in_diag2
    new_col = start_col + pieces_in_diag2
    if new_row >= 0 and new_row < board_height and new_col >= 0 and new_col < board_width:
        fields.append((new_row, new_col))

    new_fields = []
    for field_row, field_col in fields:
        if board[start_row, start_col] != board[field_row, field_col]:
            new_fields.append((field_row, field_col))



    return new_fields

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
    score, best_move = minimax(board, depth=2, alpha=-float('inf'), beta=float('inf'), maximizing_player=True)

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
    white_pieces = np.sum(board == "W")
    black_pieces = np.sum(board == "B")
    return white_pieces - black_pieces

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