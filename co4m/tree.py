"""
Simple Tree implementation for MCTS
TODO: back-up
TODO:
"""

from math import sqrt, log
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from co4m.board import Board


class Node:
    """
    Basic Node class
    """

    def __init__(
        self,
        board: "Board",
        parent: "Node" = None,
        action: int = None,
        children: List["Node"] = None,
    ):
        self.board = board
        self.sum_value = 0
        self.n_visits = 0
        self.parent = parent
        self.action = action
        self.children = children

    @property
    def value(self) -> float:
        return self.sum_value / self.n_visits

    def update(self, value):
        self.sum_value += value
        self.n_visits += 1

    # def backup(self, value):
    #     if self.parent:
    #         node = self.parent
    #         node.update(-value)
    #         node.backup(-value)

    def uct(self) -> float:
        return self.value + sqrt(2 * log(self.parent.n_visits) / self.n_visits)

    def depth(self) -> int:
        if self.children:
            return 1 + max([child.depth() for child in self.children])
        return 0
