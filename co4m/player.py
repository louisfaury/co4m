"""
Connect Four Player implementation
"""

from abc import abstractmethod
from enum import Enum

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from co4m.board import Board


class PlayerId(Enum):
    PLAYER1 = 1
    PLAYER2 = -1

    def __str__(self):
        return "Player 1" if self == PlayerId.PLAYER1 else "Player 2"


class PlayerType(Enum):
    HUMAN = 1, "human"
    AI_MINIMAX = 2, "ai_minmax"
    AI_MCTS = 3, "ai_mcts"

    def __str__(self):
        return self.value[1]


class Player:
    def __init__(self, player_id: PlayerId, player_type: PlayerType):
        self.player_id = player_id
        self.player_type = player_type

    @abstractmethod
    def act(self, board: "Board") -> int:
        raise NotImplementedError


class HumanPlayer(Player):
    """
    Human Player class
    """
    def __init__(self, player_id: PlayerId):
        super().__init__(player_id, PlayerType.HUMAN)

    def act(self, board: "Board"):
        while True:
            move = int(input(str(self.player_id) + " to move. Pick a column (1-7). "))
            if board.is_legal(move):
                return move - 1
            else:
                print("\n\033[1;91mNot a valid action.\033[0m")

    def __repr__(self):
        return str(self.player_id) + " (" + str(self.player_type) + ") "
