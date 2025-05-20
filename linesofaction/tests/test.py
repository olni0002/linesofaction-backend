import unittest
from unittest.mock import patch
import numpy as np
from linesofaction.server.game import minimax, all_possible_moves

class Test(unittest.TestCase):
    @patch("linesofaction.server.game.board_static_evaluation")
    def test_alpha_beta_pruning(self, mock_evaluate_board):
        print("Test is running!")  # Debug print statement

        # Mock evaluate_board to return a fixed value and count calls
        mock_evaluate_board.side_effect = lambda board: np.sum(board == "W") - np.sum(board == "B")

        # Create a simple board state
        board = np.array([
            ["W", "N", "N", "N", "N", "N", "N", "N"],
            ["N", "B", "N", "N", "N", "N", "N", "N"],
            ["N", "N", "N", "N", "N", "N", "N", "N"],
            ["N", "N", "N", "N", "N", "N", "N", "N"],
            ["N", "N", "N", "N", "N", "N", "N", "N"],
            ["N", "N", "N", "N", "N", "N", "N", "N"],
            ["N", "N", "N", "N", "N", "N", "N", "N"],
            ["N", "N", "N", "N", "N", "N", "N", "N"],
        ], dtype="U1")

        # Call minimax with a depth of 2
        minimax(board, 2, -float('inf'), float('inf'), True)

        # Check that evaluate_board was called fewer times than all possible moves
        total_possible_moves = len(all_possible_moves(board, "W")) * len(all_possible_moves(board, "B"))
        self.assertLess(mock_evaluate_board.call_count, total_possible_moves)

if __name__ == "__main__":
    unittest.main()
