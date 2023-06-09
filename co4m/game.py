"""
Connect Four game implementation
"""

from co4m.board import Board
from co4m.player import PlayerId


def run(render: str = "terminal"):
    """
    Running and rendering the game
    """
    board = Board()
    print(board)

    while True:
        move = int(input("Player 1 move: "))
        won = board.drop_coin(move - 1, PlayerId.PLAYER1)

        if render == "terminal":
            print(board)

        if won:
            print("Player 1 wins")
            break

        move = int(input("Player 2 move: "))
        won = board.drop_coin(move - 1, PlayerId.PLAYER2)

        if render == "terminal":
            print(board)

        if won:
            print("Player 2 wins")
            break

        if board.is_draw():
            print("'Tis a draw")
            break


if __name__ == "__main__":
    run()
