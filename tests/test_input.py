import pygame
import pytest

from snake_game.input import Action, map_key
from snake_game.logic import Direction


@pytest.mark.parametrize(
    "key, expected",
    [
        (pygame.K_UP, Direction.UP),
        (pygame.K_w, Direction.UP),
        (pygame.K_DOWN, Direction.DOWN),
        (pygame.K_s, Direction.DOWN),
        (pygame.K_LEFT, Direction.LEFT),
        (pygame.K_a, Direction.LEFT),
        (pygame.K_RIGHT, Direction.RIGHT),
        (pygame.K_d, Direction.RIGHT),
        (pygame.K_SPACE, Action.RESTART),
        (pygame.K_RETURN, Action.RESTART),
        (pygame.K_KP_ENTER, Action.RESTART),
        (pygame.K_ESCAPE, Action.QUIT),
    ],
)
def test_mapped_keys(key, expected):
    assert map_key(key) is expected


@pytest.mark.parametrize("key", [pygame.K_x, pygame.K_1, pygame.K_TAB])
def test_unmapped_key_returns_none(key):
    assert map_key(key) is None
