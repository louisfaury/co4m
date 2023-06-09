"""
Connect Four game implementation
"""
import time

from co4m.board import Board
from co4m.player import PlayerId

PLAYER_1 = PlayerId.PLAYER1
PLAYER_2 = PlayerId.PLAYER2


def toggle(player_id: PlayerId):
    return PLAYER_2 if player_id==PLAYER_1 else PLAYER_1


def run(render: str = "terminal"):
    """
    Running and rendering the game
    """
    board = Board()
    board.render(render)
    player = PLAYER_1
    while True:
        move = int(input(f"{player.name} to move. Pick a column between 1 and 7. "))
        try:
            won = board.drop_coin(move - 1, player)
        except ValueError as e:
            print(e)
            continue
            
        board.render(render)

        if won:
            print(f"{player.name} won!")
            break
        if board.is_draw():
            print("'This a draw!")
            break

        player = toggle(player)


if __name__ == "__main__":
    run()
