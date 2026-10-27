import random

import pygame
import pytest

from snake_game import config
from snake_game.logic import new_game
from snake_game.render import draw, make_fonts


@pytest.fixture(scope="module")
def env():
    pygame.init()
    fonts = make_fonts()
    surface = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    yield surface, fonts
    pygame.quit()


def cell_center(cell):
    x, y = cell
    half = config.CELL_SIZE // 2
    return (x * config.CELL_SIZE + half, y * config.CELL_SIZE + half)


def make_state():
    state = new_game(random.Random(1))
    state.food = (15, 15)  # fixed spot, away from the score text
    return state


def test_draw_normal_frame(env):
    surface, fonts = env
    state = make_state()
    draw(surface, state, fonts)
    assert surface.get_size() == (600, 600)
    assert surface.get_at(cell_center(state.snake[0]))[:3] == config.SNAKE_HEAD_COLOR
    assert surface.get_at(cell_center(state.snake[1]))[:3] == config.SNAKE_BODY_COLOR
    assert surface.get_at(cell_center(state.food))[:3] == config.FOOD_COLOR


def test_draw_game_over_overlay(env):
    surface, fonts = env
    state = make_state()
    draw(surface, state, fonts)
    normal = surface.get_at(cell_center(state.food))
    state.game_over = True
    draw(surface, state, fonts)
    assert surface.get_at(cell_center(state.food)) != normal


def test_draw_won_overlay(env):
    surface, fonts = env
    state = make_state()
    state.food = None
    state.won = True
    state.game_over = True
    draw(surface, state, fonts)
