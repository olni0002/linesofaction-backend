#!/usr/bin/env python3

from flask import Flask, request
from flask_cors import CORS
import numpy as np

import game

# Ændret til at den bruger 'W' og 'B' i stedet for '1' og '2' for at være konsistent med den øvrige kode
start_board = np.full((8, 8), 'N', dtype="U1")
start_board[0, 1:-1] = 'W'
start_board[-1, 1:-1] = 'W'
start_board[1:-1, 0] = 'B'
start_board[1:-1, -1] = 'B'

app = Flask(__name__)
CORS(app)

@app.route('/api/board/')
def get_board():
    return {'board': start_board.tolist()}

@app.route('/api/validateMove', methods=['POST'])
def validate_move():
    board = request.get_json()

    s_row = board["start_row"]
    s_col = board["start_col"]
    d_row = board["dest_row"]
    d_col = board["dest_col"]

    board = np.array(board["board"], dtype="U1")

    is_valid: bool = game.is_move_legal(s_row, s_col, d_row, d_col, board)

    return {"is_valid": is_valid}

@app.route('/api/computerMove', methods=['POST'])
def computer_move_route():
    data = request.get_json()
    board = np.array(data["board"], dtype="U1")
    computer_color = data.get("computer_color", "W")

    board, time_taken, reached_depth, node_count = game.computer_move(board, computer_color)

    board = list(map(lambda row: list(map(lambda field: None if field == "N" else field, row)), board.tolist()))
    return {
        'board': board,
        'time_taken': time_taken,
        'depth': reached_depth,
        'node_count': node_count
    }

@app.route('/api/checkResult', methods=['POST'])
def check_result():
    board = np.array(request.get_json()["board"])
    return {"winner": game.get_winner(board)}

@app.route('/api/getPossibleMoves', methods=['POST'])
def get_possible_moves():
    data = request.get_json()
    board = np.array(data["board"], dtype="U1")
    start_row = data["row"]
    start_col = data["col"]
    player_color = data["playerColor"]
    
    if board[start_row, start_col] != player_color:
        return {"possibleMoves": []}
    
    moves = game.legal_moves(start_row, start_col, board)
    
    #Convert to list of coordinate pairs
    valid_moves = [[int(move[0]), int(move[1])] for move in moves]
    
    return {"possibleMoves": valid_moves}

if __name__ == "__main__":
    app.run()
