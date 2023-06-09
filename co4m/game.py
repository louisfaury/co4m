"""
Connect Four game implementation
"""

from typing import Optional
import time

from co4m.board import Board
from co4m.player import PlayerId

PLAYER_1 = PlayerId.PLAYER1
PLAYER_2 = PlayerId.PLAYER2


def clear_console():
    print("\033c")


def toggle(player_id: PlayerId):
    """
    Change player
    """
    return PLAYER_2 if player_id == PLAYER_1 else PLAYER_1


def run(board: Optional[Board] = None):
    """
    Runs the game in the terminal
    """
    board = board if board else Board()
    player = PLAYER_1
    while True:
        clear_console()
        board.render()
        move = int(input(str(player) + " to move. Pick a column (1-7). "))
        try:
            won = board.drop_coin(move - 1, player)
        except ValueError:
            print("\n\033[1;91mNot a valid action.\033[0m")
            time.sleep(2)
            continue

        if won:
            clear_console()
            board.render()
            print(f"\n\033[1;91m{player} won!\033[0m")
            return player

        if board.is_draw():
            clear_console()
            board.render()
            print("This a draw!")
            return 0

        time.sleep(0.25)

        # change player
        player = toggle(player)


if __name__ == "__main__":
    run()
