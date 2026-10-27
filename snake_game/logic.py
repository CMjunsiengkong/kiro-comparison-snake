"""Pure game rules for Snake. No pygame imports, so everything here is unit-testable."""
from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Deque, Optional, Tuple

from snake_game import config

Cell = Tuple[int, int]
MAX_PENDING = 2


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def dx(self) -> int:
        return self.value[0]

    @property
    def dy(self) -> int:
        return self.value[1]

    @property
    def opposite(self) -> Direction:
        return _OPPOSITES[self]


_OPPOSITES = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}


@dataclass
class GameState:
    snake: Deque[Cell]  # head first
    direction: Direction
    pending: Deque[Direction] = field(default_factory=deque)
    food: Optional[Cell] = None
    score: int = 0
    game_over: bool = False
    won: bool = False
    width: int = config.GRID_WIDTH
    height: int = config.GRID_HEIGHT


def new_game(
    rng: random.Random,
    width: int = config.GRID_WIDTH,
    height: int = config.GRID_HEIGHT,
) -> GameState:
    """Return a fresh game: 3-cell snake centered, moving right, with food placed."""
    hx, hy = width // 2, height // 2
    snake = deque([(hx, hy), (hx - 1, hy), (hx - 2, hy)])
    state = GameState(snake=snake, direction=Direction.RIGHT, width=width, height=height)
    state.food = spawn_food(state, rng)
    return state


def change_direction(state: GameState, d: Direction) -> None:
    """Queue a direction change, ignoring reversals, duplicates, and overflow."""
    if state.game_over or len(state.pending) >= MAX_PENDING:
        return
    ref = state.pending[-1] if state.pending else state.direction
    if d == ref or d == ref.opposite:
        return
    state.pending.append(d)


def spawn_food(state: GameState, rng: random.Random) -> Optional[Cell]:
    """Pick a random free cell, or None if the snake fills the board. Does not assign."""
    occupied = set(state.snake)
    free = [
        (x, y)
        for y in range(state.height)
        for x in range(state.width)
        if (x, y) not in occupied
    ]
    return rng.choice(free) if free else None


def step(state: GameState, rng: random.Random) -> None:
    """Advance the game by one tick, mutating state in place."""
    if state.game_over:
        return
    if state.pending:
        state.direction = state.pending.popleft()

    hx, hy = state.snake[0]
    nxt = (hx + state.direction.dx, hy + state.direction.dy)
    eating = nxt == state.food

    x, y = nxt
    if x < 0 or x >= state.width or y < 0 or y >= state.height:
        state.game_over = True
        return

    # The tail moves away this tick unless we're eating, so it's not an obstacle.
    body = list(state.snake) if eating else list(state.snake)[:-1]
    if nxt in body:
        state.game_over = True
        return

    state.snake.appendleft(nxt)
    if eating:
        state.score += 1
        state.food = spawn_food(state, rng)
        if state.food is None:
            state.won = True
            state.game_over = True
    else:
        state.snake.pop()
