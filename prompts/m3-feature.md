Add two things to the Snake game:

1. A high score that is kept between games, even after I close the game.
2. The game gets faster as the snake grows.

So that I can test it, put the high score code in `snake_game/highscore.py` with `load_high_score(path) -> int` and `save_high_score(path, score) -> None`, where `path` is a `pathlib.Path`. Before any high score is saved, the high score is 0. Also add `speed_for_score(score) -> float` to `snake_game/logic.py`, which returns the speed in moves per second. At score 0 it is today's speed.

Update the README. You are done when `uv run pytest` passes, including tests for the new code.