"""
Connect Four game implementation
"""

from enum import Enum
import sys
import time

import pygame

from co4m.board import Board
from co4m.player import PlayerId

PLAYER_1 = PlayerId.PLAYER1
PLAYER_2 = PlayerId.PLAYER2

SQUARE_SIZE = 50
RADIUS = SQUARE_SIZE / 2
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)


class Rendering(Enum):
    NONE = 0
    TERMINAL = 1
    GRAPHICS = 2


def toggle(player_id: PlayerId):
    return PLAYER_2 if player_id == PLAYER_1 else PLAYER_1


def run_in_terminal(board: Board):
    player = PLAYER_1

    while True:
        move = int(input(f"{player.name} to move. Pick a column (1-7). "))
        try:
            won = board.drop_coin(move - 1, player)
        except ValueError as e:
            print(e)
            continue

        board.render()

        if won:
            print(f"{player.name} won!")
            return player
        if board.is_draw():
            print("This a draw!")
            return 0

        time.sleep(0.5)

        # change player
        player = toggle(player)


def init_graphics(board: Board):
    pygame.init()
    width, height = board.width * SQUARE_SIZE, (board.height + 1) * SQUARE_SIZE
    screen = pygame.display.set_mode(size=(width, height))
    screen.fill(WHITE)
    font = pygame.font.SysFont("monospace", 30)
    return screen, font


def draw_board(board: Board, screen):
    for i, row in enumerate(board.state[::-1]):
        for j, column in enumerate(row):
            if column != 0:
                color = BLUE if column == PLAYER_1.value else RED
                center = (int(SQUARE_SIZE * (j + 1 / 2)), int(SQUARE_SIZE * (i + 3 / 2)))
                pygame.draw.circle(screen, color, center, RADIUS)

    for j in range(board.width):
        pygame.draw.line(
            screen,
            BLACK,
            start_pos=(j * SQUARE_SIZE, SQUARE_SIZE),
            end_pos=(j * SQUARE_SIZE, (board.height + 1) * SQUARE_SIZE),
        )
    pygame.display.update()


def run_with_graphics(board: Board):
    screen, font = init_graphics(board)
    player = PLAYER_1
    won = False
    draw_board(board, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, GRAY, (0, 0, board.width * SQUARE_SIZE, SQUARE_SIZE))
                pos = event.pos[0]
                color = BLUE if player == PLAYER_1 else RED
                pygame.draw.circle(screen, color, (pos, RADIUS), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, GRAY, (0, 0, board.width * SQUARE_SIZE, SQUARE_SIZE))
                pos = event.pos[0]
                move = pos // SQUARE_SIZE
                if board.is_legal(move):
                    won = board.drop_coin(move, player)
                    if won:
                        label = font.render(f"{player.name} wins.", True, WHITE)
                        screen.blit(label, (0, 0))
                    draw_board(board, screen)
                    player = toggle(player)

        if won:
            pygame.time.wait(2_000)
            won = False
            player = PLAYER_1
            board.reset()
            screen.fill(WHITE)
            draw_board(board, screen)


def run(rendering=Rendering.NONE):
    """
    Running and rendering the game
    """
    board = Board()

    if rendering == Rendering.TERMINAL:
        return run_in_terminal(board)
    elif rendering == Rendering.GRAPHICS:
        return run_with_graphics(board)
    else:
        raise NotImplementedError


if __name__ == "__main__":
    run(Rendering.GRAPHICS)
