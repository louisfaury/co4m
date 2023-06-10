"""
Connect Four board implementation
"""
from copy import deepcopy
from typing import List, Literal, Tuple
import numpy as np

from co4m.player import PlayerId


class Board:
    """
    Connect Four Board class
    """

    def __init__(self):
        self.width = 7
        self.height = 6
        self.state = np.zeros(shape=(self.height, self.width))
        self.int_to_char = {1: "\U0001F7E1", -1: "\U0001F534", 0: "\u2B24"}

    def get_height(self, column: int) -> int:
        """
        Current height of a column
        """
        return int(np.sum(np.abs(self.state[:, column])))

    def is_legal(self, column: int) -> bool:
        """
        Checks if adding a coin to `column` is a legal move
        """
        if column < 0 or column >= self.width:
            return False
        return self.get_height(column) < self.height

    def drop_coin(
        self, column: int, player_id: Literal[PlayerId.PLAYER1, PlayerId.PLAYER2]
    ) -> bool:
        """
        Drops a coin in `column`
        """
        if not self.is_legal(column):
            raise ValueError(f"Cannot insert coin in column {column}")

        self.state[self.get_height(column), column] = player_id.value

        return self.is_won(player_id)

    @staticmethod
    def max_consecutive(array: list):
        """
        Given a boolean array, find the max. of consecutive `True` value
        """
        value, max_value = 0, 0
        for elem in array:
            value = value + 1 if elem else 0
            max_value = max(max_value, value)
        return max_value

    def is_won(self, player_id: PlayerId) -> bool:
        """
        Checks if the game is won for a particular player
        """
        conditional_state = self.state == player_id.value
        if np.sum(np.abs(conditional_state)) < 4:
            return False

        check_list = (
            [conditional_state[:, column] for column in range(self.width)]
            + [conditional_state[row, :] for row in range(self.height)]
            + [conditional_state.diagonal(offset) for offset in [-3, -2, -1, 0, 1, 2, 3]]
            + [np.fliplr(conditional_state).diagonal(offset) for offset in [-3, -2, -1, 0, 1, 2, 3]]
        )

        max_consec = 0
        for array in check_list:
            max_consec = max(max_consec, self.max_consecutive(array))

        return max_consec >= 4

    def is_draw(self):
        """
        Checks if the game is a draw
        """
        return (
            np.sum(np.abs(self.state)) == self.width * self.height
            and not self.is_won(PlayerId.PLAYER1)
            and not self.is_won(PlayerId.PLAYER2)
        )

    def get_legal_moves(self) -> List[int]:
        """
        Returns all legal moves
        """
        return [move for move in range(self.width) if self.is_legal(move)]

    def is_terminal(self):
        """ "
        Checks if state is terminal (win, loose or draw)
        """
        return self.is_won(PlayerId.PLAYER1) or self.is_won(PlayerId.PLAYER2) or self.is_draw()

    def reset(self):
        self.state *= 0

    def expand(self, player_id: PlayerId) -> Tuple[List[int], List["Board"]]:
        """
        Expand the board from its current state to reachable valid states
        """
        valid_moves = self.get_legal_moves()
        valid_children = []
        for move in valid_moves:
            next_board = deepcopy(self)
            next_board.drop_coin(move, player_id)
            valid_children.append(next_board)
        return valid_moves, valid_children

    def __repr__(self):
        return str(self.state[::-1])

    def __str__(self):
        descr = "\n\033[1;30;47m"
        descr += "\n   \t \t \t \t \t \t   \n".join(
            [
                " " + "\t".join([self.int_to_char[elem] for i, elem in enumerate(row)]) + "  "
                for row in self.state[::-1]
            ]
        )
        descr += "\n"
        descr += "\n"
        descr += "\n\033[0;0m"
        return descr
