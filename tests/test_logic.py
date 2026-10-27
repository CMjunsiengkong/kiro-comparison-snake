import random
from collections import deque

import pytest

from snake_game.logic import (
    Direction,
    GameState,
    change_direction,
    new_game,
    spawn_food,
    step,
)


def make_state(snake, direction, food=None, width=20, height=20):
    return GameState(deque(snake), direction, deque(), food, width=width, height=height)


@pytest.fixture
def rng():
    return random.Random(0)


def test_direction_vectors_and_opposites():
    assert (Direction.UP.dx, Direction.UP.dy) == (0, -1)
    assert (Direction.DOWN.dx, Direction.DOWN.dy) == (0, 1)
    assert (Direction.LEFT.dx, Direction.LEFT.dy) == (-1, 0)
    assert (Direction.RIGHT.dx, Direction.RIGHT.dy) == (1, 0)
    assert Direction.UP.opposite is Direction.DOWN
    assert Direction.DOWN.opposite is Direction.UP
    assert Direction.LEFT.opposite is Direction.RIGHT
    assert Direction.RIGHT.opposite is Direction.LEFT


def test_new_game_initial_state(rng):
    state = new_game(rng)
    assert list(state.snake) == [(10, 10), (9, 10), (8, 10)]
    assert state.direction is Direction.RIGHT
    assert state.score == 0
    assert state.game_over is False
    assert state.won is False
    assert len(state.pending) == 0
    assert state.food is not None
    assert state.food not in state.snake


def test_restart_new_game_resets(rng):
    state = new_game(rng)
    state.score = 5
    state.game_over = True
    state.won = True
    state = new_game(rng)
    assert state.score == 0
    assert len(state.snake) == 3
    assert state.game_over is False
    assert state.won is False


@pytest.mark.parametrize(
    "snake, direction",
    [
        ([(10, 10), (9, 10), (8, 10)], Direction.RIGHT),
        ([(10, 10), (11, 10), (12, 10)], Direction.LEFT),
        ([(10, 10), (10, 11), (10, 12)], Direction.UP),
        ([(10, 10), (10, 9), (10, 8)], Direction.DOWN),
    ],
)
def test_move(rng, snake, direction):
    state = make_state(snake, direction, food=(0, 0))
    tail = snake[-1]
    step(state, rng)
    assert state.snake[0] == (10 + direction.dx, 10 + direction.dy)
    assert len(state.snake) == 3
    assert tail not in state.snake
    assert state.game_over is False


def test_reversal_rejected(rng):
    state = make_state([(10, 10), (9, 10), (8, 10)], Direction.RIGHT, food=(0, 0))
    change_direction(state, Direction.LEFT)
    assert len(state.pending) == 0
    step(state, rng)
    assert state.direction is Direction.RIGHT
    assert state.snake[0] == (11, 10)


def test_ninety_degree_turn(rng):
    state = make_state([(10, 10), (9, 10), (8, 10)], Direction.RIGHT, food=(0, 0))
    change_direction(state, Direction.UP)
    step(state, rng)
    assert state.direction is Direction.UP
    assert state.snake[0] == (10, 9)


def test_two_queued_turns_apply_over_two_ticks(rng):
    state = make_state([(10, 10), (9, 10), (8, 10)], Direction.RIGHT, food=(0, 0))
    change_direction(state, Direction.UP)
    change_direction(state, Direction.LEFT)
    step(state, rng)
    assert state.direction is Direction.UP
    assert state.snake[0] == (10, 9)
    step(state, rng)
    assert state.direction is Direction.LEFT
    assert state.snake[0] == (9, 9)
    assert state.game_over is False


def test_opposite_of_queued_rejected():
    state = make_state([(10, 10), (9, 10), (8, 10)], Direction.RIGHT)
    change_direction(state, Direction.UP)
    change_direction(state, Direction.DOWN)
    assert list(state.pending) == [Direction.UP]


def test_duplicate_direction_rejected():
    state = make_state([(10, 10), (9, 10), (8, 10)], Direction.RIGHT)
    change_direction(state, Direction.RIGHT)
    assert len(state.pending) == 0
    change_direction(state, Direction.UP)
    change_direction(state, Direction.UP)
    assert list(state.pending) == [Direction.UP]


def test_queue_max_two():
    state = make_state([(10, 10), (9, 10), (8, 10)], Direction.RIGHT)
    change_direction(state, Direction.UP)
    change_direction(state, Direction.LEFT)
    change_direction(state, Direction.DOWN)
    assert list(state.pending) == [Direction.UP, Direction.LEFT]


def test_food_never_on_snake():
    long_snake = [(x, 5) for x in range(20)] + [(x, 6) for x in range(19, -1, -1)]
    for seed in range(200):
        state = new_game(random.Random(seed))
        assert state.food is not None
        assert state.food not in state.snake

        custom = make_state(long_snake, Direction.RIGHT)
        food = spawn_food(custom, random.Random(seed))
        assert food is not None
        assert food not in custom.snake
        fx, fy = food
        assert 0 <= fx < custom.width and 0 <= fy < custom.height


def test_spawn_food_returns_none_when_full(rng):
    state = make_state([(1, 0), (0, 0)], Direction.RIGHT, width=2, height=1)
    assert spawn_food(state, rng) is None


def test_eating_grows_scores_and_respawns(rng):
    state = make_state([(10, 10), (9, 10), (8, 10)], Direction.RIGHT, food=(11, 10))
    step(state, rng)
    assert len(state.snake) == 4
    assert state.score == 1
    assert state.snake[0] == (11, 10)
    assert state.food is not None
    assert state.food not in state.snake
    assert state.game_over is False


def test_full_board_win(rng):
    state = make_state([(1, 0), (0, 0)], Direction.RIGHT, food=(2, 0), width=3, height=1)
    step(state, rng)
    assert len(state.snake) == 3
    assert state.score == 1
    assert state.food is None
    assert state.won is True
    assert state.game_over is True


@pytest.mark.parametrize(
    "snake, direction",
    [
        ([(19, 10), (18, 10), (17, 10)], Direction.RIGHT),
        ([(0, 10), (1, 10), (2, 10)], Direction.LEFT),
        ([(10, 0), (10, 1), (10, 2)], Direction.UP),
        ([(10, 19), (10, 18), (10, 17)], Direction.DOWN),
    ],
)
def test_wall_collision(rng, snake, direction):
    state = make_state(snake, direction, food=(5, 5))
    step(state, rng)
    assert state.game_over is True
    assert state.won is False
    assert list(state.snake) == snake


def test_self_collision(rng):
    snake = [(5, 5), (6, 5), (6, 6), (5, 6), (4, 6)]
    state = make_state(snake, Direction.DOWN, food=(0, 0))
    step(state, rng)
    assert state.game_over is True
    assert list(state.snake) == snake


def test_chasing_tail_allowed(rng):
    state = make_state([(5, 5), (6, 5), (6, 6), (5, 6)], Direction.DOWN, food=(0, 0))
    step(state, rng)
    assert state.game_over is False
    assert state.snake[0] == (5, 6)
    assert len(state.snake) == 4


def test_tail_cell_blocked_when_eating(rng):
    state = make_state([(5, 5), (6, 5), (6, 6), (5, 6)], Direction.DOWN, food=(5, 6))
    step(state, rng)
    assert state.game_over is True


def test_step_after_game_over_noop(rng):
    state = make_state([(10, 10), (9, 10), (8, 10)], Direction.RIGHT, food=(0, 0))
    state.game_over = True
    snapshot = (list(state.snake), state.score, state.food, state.direction)
    change_direction(state, Direction.UP)
    assert len(state.pending) == 0
    step(state, rng)
    assert (list(state.snake), state.score, state.food, state.direction) == snapshot
    assert state.game_over is True
