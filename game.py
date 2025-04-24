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
