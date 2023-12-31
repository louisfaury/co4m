"""
Connect Four Player implementation
"""

from abc import abstractmethod
from enum import Enum
import random
from typing import Optional, TYPE_CHECKING

import numpy as np
from co4m.tree import Node

if TYPE_CHECKING:
    from co4m.board import Board


class PlayerId(Enum):
    PLAYER1 = 1
    PLAYER2 = -1

    def __str__(self):
        return "\033[33mPlayer 1\033[0m" if self == PlayerId.PLAYER1 else "\033[31mPlayer 2\033[0m"

    def __invert__(self):
        return PlayerId.PLAYER2 if self.value == PlayerId.PLAYER1.value else PlayerId.PLAYER1


class PlayerType(Enum):
    HUMAN = "human"
    RANDOM = "random"
    AI_MINMAX = "ai_minmax"
    AI_MCTS = "ai_mcts"

    def __str__(self):
        return self.value


WIN_VALUE = 1_000

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
        print(f"{self.player_id} thinking..")
        return 0

    def __repr__(self):
        return str(self.player_id) + " (" + str(self.player_type) + ")"


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

    def __init__(self, player_id: PlayerId, depth: int = 6):
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
            return -WIN_VALUE

        if board.is_draw():
            return 0

        return float(
            np.sum(EVAL * (board.state == self.player_id.value).astype(int))
            - np.sum(EVAL * (board.state == (~self.player_id).value).astype(int))
        )

    def act(self, board: "Board", depth: Optional[int] = None) -> int:
        print(f"{self} thinking..", end="\r")
        depth = depth if depth else self.depth
        moves, children = board.expand(self.player_id)
        values = [self.minimax(child, depth - 1) for child in children]
        # print(moves, values)
        # input("move")
        return moves[int(np.argmax(values))]

    def minimax(
        self,
        board: "Board",
        depth: int,
        max_node: bool = False,
        alpha: float = -WIN_VALUE,
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
                    value = max(value, self.minimax(child, depth - 1, not max_node, value, beta))
                    if value >= beta:
                        return beta
                return value
            else:
                value = beta
                for child in children:
                    value = min(value, self.minimax(child, depth - 1, not max_node, alpha, value))
                    if value <= alpha:
                        return alpha
                return value

    def __repr__(self):
        return super().__repr__()[:-1] + f" - depth={self.depth})"


class MctsPlayer(Player):
    """
    Monte Carlo Tree Search class
    """

    def __init__(self, player_id: PlayerId, max_iter: int = 1_000):
        super().__init__(player_id, PlayerType.AI_MCTS)
        self.max_iter = max_iter

    def act(self, board):
        print(f"{self} thinking..")
        node = Node(board)
        for _ in range(self.max_iter):
            self.mcts(node, self.player_id)
        # for child in node.children:
        #     print(child.action, np.around(child.value, 2), child.depth(), child.n_visits)
        # input("move")
        best_child = sorted(node.children, key=lambda child: child.value)[-1]
        return best_child.action

    def mcts(self, node: Node, player_id: PlayerId):
        """
        Monte-Carl Tree search
        """
        # Tree policy
        exploit = True
        is_terminal = False
        while exploit and not is_terminal:
            if node.fully_explored():
                node = sorted(node.children, key=lambda child: child.uct(), reverse=True)[0]
            else:
                exploit = False
                if not node.children:
                    moves, boards = node.board.expand(player_id)
                    node.children = [
                        Node(child, parent=node, action=move) for move, child in zip(moves, boards)
                    ]
                node = random.choice([child for child in node.children if child.n_visits == 0])
            is_terminal = node.board.is_terminal()
            player_id = ~player_id

        # Default policy
        node.is_terminal = is_terminal
        reward = -self.roll_out(node, player_id)
        node.backup(reward)

    def roll_out(self, node: Node, player_id: PlayerId):
        """
        Perform random roll-out (if node is not terminal)
        Returns
        -------
        1 if player_id wins, 0 if draw, -1 otherwise
        """

        if node.is_terminal:
            if node.board.is_draw():
                return 0
            else:
                return 1 if node.board.is_won(player_id) else -1

        turn = player_id
        board = node.board.copy()  # save time by copying
        # roll-out
        while True:
            winning_move = board.is_winning_move(turn)  # checks if there exist a winning move
            move = (
                winning_move
                if winning_move >= 0
                else random.choice(board.get_legal_moves())  # else play random move
            )
            won = board.drop_coin(move, turn)

            if won:
                return 1 if turn == player_id else -1
            if board.is_draw():
                return 0

            turn = ~turn

    def __repr__(self):
        return super().__repr__()[:-1] + f" - max_iter={self.max_iter})"


def from_player_type(player_type: PlayerType):
    """
    Player factory
    """
    if player_type == PlayerType.HUMAN:
        return HumanPlayer
    if player_type == PlayerType.AI_MINMAX:
        return MinimaxPlayer
    if player_type == PlayerType.RANDOM:
        return RandomPlayer
    if player_type == PlayerType.AI_MCTS:
        return MctsPlayer
    else:
        raise ValueError("Unknown player type")
