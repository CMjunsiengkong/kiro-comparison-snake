"""Draw the game state onto a pygame surface."""
from __future__ import annotations

import pygame

from snake_game import config
from snake_game.logic import Cell, GameState


class Fonts:
    """Holds the fonts used for on-screen text."""

    def __init__(self, score: pygame.font.Font, big: pygame.font.Font, small: pygame.font.Font):
        self.score = score
        self.big = big
        self.small = small


def make_fonts() -> Fonts:
    """Build fonts from pygame's bundled default font. Call after pygame.font.init()."""
    return Fonts(
        score=pygame.font.Font(None, 32),
        big=pygame.font.Font(None, 72),
        small=pygame.font.Font(None, 28),
    )


def _cell_rect(cell: Cell) -> pygame.Rect:
    x, y = cell
    size = config.CELL_SIZE
    # Inset by 1px so adjacent cells stay visually distinct.
    return pygame.Rect(x * size, y * size, size, size).inflate(-2, -2)


def _draw_grid(surface: pygame.Surface, state: GameState) -> None:
    size = config.CELL_SIZE
    width_px = state.width * size
    height_px = state.height * size
    for x in range(1, state.width):
        pygame.draw.line(surface, config.GRID_COLOR, (x * size, 0), (x * size, height_px))
    for y in range(1, state.height):
        pygame.draw.line(surface, config.GRID_COLOR, (0, y * size), (width_px, y * size))


def draw(surface: pygame.Surface, state: GameState, fonts: Fonts) -> None:
    """Render one full frame."""
    surface.fill(config.BACKGROUND_COLOR)
    _draw_grid(surface, state)

    if state.food is not None:
        pygame.draw.rect(surface, config.FOOD_COLOR, _cell_rect(state.food))

    for i, cell in enumerate(state.snake):
        color = config.SNAKE_HEAD_COLOR if i == 0 else config.SNAKE_BODY_COLOR
        pygame.draw.rect(surface, color, _cell_rect(cell))

    score_text = fonts.score.render("Score: {}".format(state.score), True, config.TEXT_COLOR)
    surface.blit(score_text, (10, 8))

    if state.game_over:
        draw_overlay(surface, state, fonts)


def draw_overlay(surface: pygame.Surface, state: GameState, fonts: Fonts) -> None:
    """Dim the board and show the end-of-game message."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill(config.OVERLAY_COLOR)
    surface.blit(overlay, (0, 0))

    cx = surface.get_width() // 2
    cy = surface.get_height() // 2
    lines = [
        (fonts.big, "You Win" if state.won else "Game Over", cy - 60),
        (fonts.score, "Final score: {}".format(state.score), cy),
        (fonts.small, "Space/Enter to restart, Esc to quit", cy + 45),
    ]
    for font, text, y in lines:
        rendered = font.render(text, True, config.TEXT_COLOR)
        surface.blit(rendered, rendered.get_rect(center=(cx, y)))
