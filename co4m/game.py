"""
Connect Four game implementation
"""

from typing import Optional
import time

from co4m.board import Board
from co4m.player import HumanPlayer, PlayerId


def clear_console():
    print("\033c")


def run(board: Optional[Board] = None):
    """
    Runs the game in the terminal
    """
    board = board if board else Board()
    players = tuple(HumanPlayer(player_id) for player_id in PlayerId)
    n_round = 0

    while True:
        clear_console()
        board.render()
        player = players[n_round % 2]
        move = player.act(board)
        won = board.drop_coin(move, player.player_id)

        if won:
            clear_console()
            board.render()
            print(f"\033[1;91m{player} won!\033[0m")
            return player

        if board.is_draw():
            clear_console()
            board.render()
            print("This a draw!")
            return 0

        n_round += 1
        time.sleep(0.1)


if __name__ == "__main__":
    run()
