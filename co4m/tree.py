"""
Simple Tree implementation for MCTS
TODO: back-up
"""

from math import sqrt, log
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from co4m.board import Board


class Node:
    """
    Basic Node class
    """

    def __init__(
        self,
        board: "Board",
        parent: Optional["Node"] = None,
        action: Optional[int] = None,
        children: Optional[List["Node"]] = None,
    ):
        self.board = board
        self.sum_value = 0
        self.n_visits = 0
        self.parent = parent
        self.action = action
        self.children = children
        self.is_terminal = False

    @property
    def value(self) -> float:
        return self.sum_value / self.n_visits

    def backup(self, reward: int):
        self.sum_value += reward
        self.n_visits += 1
        parent = self.parent
        if parent:
            reward *= -1
            parent.backup(reward)

    def uct(self) -> float:
        if self.is_terminal:
            return self.value
        return self.value + sqrt(2 * log(self.parent.n_visits) / self.n_visits)

    def depth(self) -> int:
        if self.children:
            return 1 + max(child.depth() for child in self.children)
        return 0

    def fully_explored(self) -> bool:
        if self.children:
            return min(child.n_visits for child in self.children) > 0
        return False
