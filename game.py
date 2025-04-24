import numpy as np

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

    lines = ((row,"row"), (col,"col"), (diag1,"diag1"),
             (diag2,"diag2"))

    for line in lines:
        pieces_in_line = 0
        for i in line[0]:
            if i != 'N':
                pieces_in_line += 1


        new_positions = []

        line_type = line[1]
        if line_type == "row":
            new_positions.append((start_row,start_col+pieces_in_line))
            new_positions.append((start_row,start_col-pieces_in_line))
        elif line_type == "col":
            new_positions.append((start_row+pieces_in_line,start_col))
            new_positions.append((start_row-pieces_in_line,start_col))
        elif line_type == "diag1":
            new_positions.append((start_row-pieces_in_line,start_col+pieces_in_line))
            new_positions.append((start_row+pieces_in_line,start_col-pieces_in_line))
        elif line_type == "diag2":
            new_positions.append((start_row+pieces_in_line,start_col+pieces_in_line))
            new_positions.append((start_row-pieces_in_line,start_col-pieces_in_line))

        for row_index, col_index in new_positions:
            is_in_vertical_bounds = row_index >= 0 and row_index < board_height
            is_in_horizontal_bounds = col_index >= 0 and col_index < board_width

            not_on_ally_piece = False
            if is_in_vertical_bounds and is_in_horizontal_bounds:
                not_on_ally_piece = board[start_row, start_col] != board[row_index, col_index]

            if not_on_ally_piece:
                fields.append((row_index,col_index))


    return fields


def is_move_legal(start_row, start_col, dest_row, dest_col, board) -> bool:
    board = np.array(board, dtype="U1")



    if (dest_row, dest_col) in legal_moves(start_row, start_col, board):
        return True
    else:
        return False

def computer_move(board) -> np.ndarray:

    board = np.array(board, dtype="U1")
    piece_coordinates = []

    for row_index, row in enumerate(board):
        for col_index, field in enumerate(row):
            if board[row_index, col_index] == 'W':
                piece_coordinates.append((row_index, col_index))

    moves = []
    for row_index, col_index in piece_coordinates:
        dest = legal_moves(row_index, col_index, board)

        moves.append((row_index, col_index, dest))

    best_move = moves[0]

    board[best_move[0],best_move[1]] = "N"
    board[best_move[2][0][0],best_move[2][0][1]] = "W"

    return board
