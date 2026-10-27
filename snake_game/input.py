"""Map pygame key codes to game directions or actions."""
from __future__ import annotations

from enum import Enum
from typing import Optional, Union

import pygame

from snake_game.logic import Direction


class Action(Enum):
    RESTART = "restart"
    QUIT = "quit"


KEY_MAP = {
    pygame.K_UP: Direction.UP,
    pygame.K_w: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_s: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_a: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT,
    pygame.K_d: Direction.RIGHT,
    pygame.K_SPACE: Action.RESTART,
    pygame.K_RETURN: Action.RESTART,
    pygame.K_KP_ENTER: Action.RESTART,
    pygame.K_ESCAPE: Action.QUIT,
}


def map_key(key: int) -> Optional[Union[Direction, Action]]:
    """Return the Direction or Action for a key, or None if the key is unmapped."""
    return KEY_MAP.get(key)
