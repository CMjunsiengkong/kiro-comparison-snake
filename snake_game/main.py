"""Entry point: run with `python -m snake_game.main`."""
from __future__ import annotations

import random

import pygame

from snake_game import config, logic, render
from snake_game.input import Action, map_key
from snake_game.logic import Direction


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.WINDOW_TITLE)
    clock = pygame.time.Clock()
    rng = random.Random()
    fonts = render.make_fonts()
    state = logic.new_game(rng)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                action = map_key(event.key)
                if isinstance(action, Direction):
                    logic.change_direction(state, action)
                elif action is Action.RESTART and state.game_over:
                    state = logic.new_game(rng)
                elif action is Action.QUIT:
                    running = False
        if not running:
            break

        logic.step(state, rng)
        render.draw(screen, state, fonts)
        pygame.display.flip()
        clock.tick(config.TICKS_PER_SECOND)

    pygame.quit()


if __name__ == "__main__":
    main()
