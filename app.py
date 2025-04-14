from flask import Flask
import numpy as np

start_board = np.zeros((8,8))
start_board[[0,-1],1:-1] = 1
start_board[1:-1,[0,-1]] = 2

app = Flask(__name__)


@app.route('/')
def getBoard():
    return {'board': start_board.tolist()}
