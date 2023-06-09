"""
Connect Four board implementation
"""

from typing import Literal, Optional
import numpy as np

from co4m.player import PlayerId


def max_consecutive(array: list):
    """
    Given a boolean array, find the max. of consecutive `True` value
    """
    value, max_value = 0, 0
    for elem in array:
        value = value + 1 if elem else 0
        max_value = max(max_value, value)
    return max_value


class Board:
    """
    Connect Four Board class
    """

    def __init__(self):
        self.width = 7
        self.height = 6
        self.state = np.zeros(shape=(self.height, self.width))

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
            max_consec = max(max_consec, max_consecutive(array))

        return max_consec == 4

    def is_draw(self):
        """
        Checks if the game is a draw
        """
        return (
            np.sum(np.abs(self.state)) == self.width * self.height
            and not self.is_won(PlayerId.PLAYER1)
            and not self.is_won(PlayerId.PLAYER2)
        )

    def is_terminal(self) -> bool:
        """
        Checks if the board is in terminal state
        """
        return self.is_won(PlayerId.PLAYER1) or self.is_won(PlayerId.PLAYER2) or self.is_draw()

    def render(self, render: Optional[str] = None):
        """
        Rendering
        """
        if render:
            if render == "terminal":
                print(self)

    def __repr__(self):
        int_to_char = {1: "x", -1: "o", 0: "."}
        descr = "\t".join(map(str, np.arange(1, self.width + 1)))
        descr += "\n"
        descr += "".join(["-" for _ in range(50)])
        descr += "\n"
        descr += "\n".join(
            ["\t".join([int_to_char[elem] for elem in row]) for row in self.state[::-1]]
        )
        descr += "\n"
        descr += "".join(["-" for _ in range(50)])
        return descr
