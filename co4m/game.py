"""
Connect Four game implementation

TODO: play-offs against random just to be sure
TODO: auto most of the code
TODO: clean player_id attribuation
"""

from typing import Optional
import time

from co4m.board import Board
from co4m.player import MinimaxPlayer, PlayerId, HumanPlayer


def run(board: Optional[Board] = None, rendering: bool = True):
    """
    Runs the game in the terminal
    """
    board = board if board else Board()
    player_1 = MinimaxPlayer(PlayerId.PLAYER1, depth=5)
    player_2 = HumanPlayer(PlayerId.PLAYER2)

    def render():
        if rendering:
            print("\033c")  # clear terminal
            header = f"{player_1} vs {player_2}\n"
            print(header)
            print(board)

    turn = PlayerId.PLAYER1
    while True:
        render()
        player = player_1 if player_1.player_id == turn else player_2
        move = player.act(board)
        won = board.drop_coin(move, turn)

        if won:
            render()
            print(f"\033[1;91m{player} won!\033[0m")
            return player

        if board.is_draw():
            render()
            print("This a draw!")
            return 0

        turn = ~turn
        if rendering:
            time.sleep(0.2)


if __name__ == "__main__":
    run()
