# python_snake_game_model_test.py
# author: Robin Jiang
#
# this is the unittesting for the python snake game model

import unittest
from python_snake_game_model import *


class TestSnakeGameState(unittest.TestCase):
    """Tests the SnakeGameState"""
    def setUp(self):
        self._game = SnakeGameState()

    def test_new_game_starts_with_blank_board(self):
        correct_board = []
        for i in range(10):
            correct_board.append([])
            for j in range(10):
                correct_board[i].append(" ")
        correct_board = _blockify(correct_board)

        for i in range(10):
            for j in range(10):
                self.assertEqual(correct_board[i][j], self._game.get_board()[i][j])


def _blockify(board: list[list[str]]) -> list[list[Block]]:
    copy_board = []
    for i in range(len(board)):
        copy_board.append([])
        for j in range(len(board[0])):
            copy_board[i].append(Block(board[i][j]))
    return copy_board


if __name__ == "__main__":
    unittest.main()
