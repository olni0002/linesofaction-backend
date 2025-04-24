#!/usr/bin/env python3

from flask import Flask, request
from flask_cors import CORS
import numpy as np

import game

start_board = np.zeros((8,8), dtype="uint8")
start_board[[0,-1],1:-1] = 1
start_board[1:-1,[0,-1]] = 2

app = Flask(__name__)
CORS(app)

@app.route('/api/board/')
def get_board():
    return {'board': start_board.tolist()}

@app.route('/api/validateMove', methods=['POST'])
def validate_move():
    board = request.get_json()

    is_valid: bool = game.is_move_legal(board["start_row"], board["start_col"], board["dest_row"],
                                        board["dest_col"], board["board"])
    return {"is_valid": is_valid}

@app.route('/api/computerMove', methods=['POST'])
def computer_move():
    board = request.get_json()["board"]

    board = game.computer_move(np.array(board, dtype="U1"))

    board = list(map(lambda row: list(map(lambda field: None if field == "N" else field, row)), board.tolist()))
    return {'board': board}


if __name__ == "__main__":
    app.run()
