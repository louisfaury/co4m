"""
Connect Four game implementation
TODO: improve min-max heuristic
TODO: play-offs
TODO: many sanity checks
"""

from typing import Optional
import time
import sys

from co4m.board import Board
from co4m.player import Player, PlayerId, PlayerType, from_player_type


def run(player_1: Player, player_2: Player, board: Optional[Board] = None, rendering: bool = True):
    """
    Runs a connect-four game
    """
    board = board if board else Board()

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
            if rendering:
                print(f"\033[1;91m{player} won!\033[0m")
            return player.player_id.value

        if board.is_draw():
            render()
            if rendering:
                print("This a draw!")
            return 0

        turn = ~turn
        if rendering:
            time.sleep(0.2)


def cli_run():
    """
    Command Line Interface game
    """
    try:
        print("\033c")  # clear terminal
        print("\033[1mWelcome to Connect Four Master!\033[0m")
        time.sleep(1)

        valid_inputs = list(map(str, PlayerType))
        while True:
            player_1_type = str(input(f"Who is player 1? ({'/'.join(valid_inputs)}) "))
            if player_1_type in valid_inputs:
                player_1 = from_player_type(PlayerType[player_1_type.upper()])(PlayerId.PLAYER1)
                break
            print("Invalid input, try again: ")

        while True:
            player_2_type = str(input(f"Who is player 2? ({'/'.join(valid_inputs)}) "))
            if player_2_type in valid_inputs:
                player_2 = from_player_type(PlayerType[player_2_type.upper()])(PlayerId.PLAYER2)
                break
            print("Invalid input, try again: ")

        print("\033[1;91mLet's play!\033[0m")
        time.sleep(1)
        run(player_1, player_2, rendering=True)
    except KeyboardInterrupt:
        print("\nQuitting...")
        time.sleep(1)
        sys.exit(0)


if __name__ == "__main__":
    cli_run()
