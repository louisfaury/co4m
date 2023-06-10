"""
Connect Four Player implementation
"""
import random
from abc import abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from co4m.board import Board


class PlayerId(Enum):
    PLAYER1 = 1
    PLAYER2 = -1

    def __str__(self):
        return "Player 1" if self == PlayerId.PLAYER1 else "Player 2"

    def __invert__(self):
        return PlayerId.PLAYER2 if self.value == PlayerId.PLAYER1.value else PlayerId.PLAYER1


class PlayerType(Enum):
    HUMAN = "human"
    RANDOM = "random"
    AI_MINMAX = "ai_minmax"
    AI_MCTS = "ai_mcts"

    def __str__(self):
        return self.value


WIN_VALUE = 150
LOOSE_VALUE = -150

EVAL = np.array(
    [
        [3, 4, 5, 7, 5, 4, 3],
        [4, 6, 8, 10, 8, 6, 4],
        [5, 8, 11, 13, 11, 8, 5],
        [5, 8, 11, 13, 11, 8, 5],
        [4, 6, 8, 10, 8, 6, 4],
        [3, 4, 5, 7, 5, 4, 3],
    ]
)


class Player:
    """
    Basic Player class
    """

    def __init__(self, player_id: PlayerId, player_type: PlayerType):
        self.player_id = player_id
        self.player_type = player_type

    @abstractmethod
    def act(self, board: "Board") -> int:
        raise NotImplementedError

    def __repr__(self):
        return str(self.player_id) + " (" + str(self.player_type) + ") "


class HumanPlayer(Player):
    """
    Human Player class
    """

    def __init__(self, player_id: PlayerId):
        super().__init__(player_id, PlayerType.HUMAN)

    def act(self, board: "Board"):
        while True:
            move = int(input(str(self.player_id) + " to move. Pick a column (1-7). ")) - 1
            if board.is_legal(move):
                return move
            else:
                print("\n\033[1;91mNot a valid action.\033[0m")


class RandomPlayer(Player):
    """
    Random Player class
    """

    def __init__(self, player_id: PlayerId):
        super().__init__(player_id, PlayerType.RANDOM)

    def act(self, board: "Board"):
        while True:
            move = random.choice(range(board.width))
            if board.is_legal(move):
                return move


class MinimaxPlayer(Player):
    """
    Minimax player, with heuristic evaluation and alpha-beta pruning
    """

    def __init__(self, player_id: PlayerId, depth: int = 5):
        super().__init__(player_id, PlayerType.AI_MINMAX)
        self.depth = depth

    def evaluate(self, board: "Board") -> float:
        """
        Evaluation of the current board
        Use heuristic if the state is not terminal, borrowed from:
        Research on Different Heuristics for Minimax Algorithm: Insight from Connect 4_Game
        by Kang & al.
        """
        if board.is_won(self.player_id):
            return WIN_VALUE

        if board.is_won(~self.player_id):
            return LOOSE_VALUE

        if board.is_draw():
            return 0

        return float(
            np.sum(EVAL * (board.state == self.player_id.value).astype(int))
            - np.sum(EVAL * (board.state == (~self.player_id).value).astype(int))
        )

    def act(self, board: "Board", depth: int = None) -> int:
        depth = depth if depth else self.depth
        moves, children = board.expand(self.player_id)
        values = [self.minimax(child, depth - 1) for child in children]
        return moves[int(np.argmax(values))]

    def minimax(
        self,
        board: "Board",
        depth: int,
        max_node: bool = False,
        alpha: float = LOOSE_VALUE,
        beta: float = WIN_VALUE,
    ) -> float:
        """
        Minimimax implentation with alpha-beta pruning
        """
        if depth == 0 or board.is_terminal():
            return self.evaluate(board)

        else:
            children = board.expand(self.player_id if max_node else ~self.player_id)[1]
            if max_node:
                value = alpha
                for child in children:
                    value = max(value, self.minimax(child, depth - 1, ~max_node, value, beta))
                    if value >= beta:
                        return beta
                return value
            else:
                value = beta
                for child in children:
                    value = min(value, self.minimax(child, depth - 1, ~max_node, alpha, value))
                    if value <= alpha:
                        return alpha
                return value


def from_player_type(player_type: PlayerType):
    if player_type == PlayerType.HUMAN:
        return HumanPlayer
    if player_type == PlayerType.AI_MINMAX:
        return MinimaxPlayer
    if player_type == PlayerType.RANDOM:
        return RandomPlayer
    else:
        raise ValueError("Unknown player type")
