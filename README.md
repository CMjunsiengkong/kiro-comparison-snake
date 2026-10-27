# Snake

A classic Snake game for the desktop, written in Python with [Pygame](https://www.pygame.org/).
Steer the snake, eat the food, and grow as long as you can without crashing.

## Requirements

- [uv](https://docs.astral.sh/uv/). It installs the right Python (3.12) and the dependencies for you.

## Run the game

```zsh
uv run python -m snake_game.main
```

## Run the tests

```zsh
uv run pytest
```

## Controls

| Key                | Action                     |
| ------------------ | -------------------------- |
| Arrow keys / WASD  | Move                       |
| Space / Enter      | Restart after game over    |
| Esc                | Quit                       |

## Rules

- The snake moves on a 20x20 grid at a fixed 10 moves per second.
- Eat the red food to grow by one segment and score one point.
- Hitting a wall or your own body ends the game.
- Fill the whole board to win.

## Project layout

```
snake_game/
  config.py   # grid size, speed, colors
  logic.py    # game rules (no pygame, fully unit-tested)
  input.py    # keyboard -> direction/action mapping
  render.py   # drawing
  main.py     # window and game loop
tests/        # pytest suite
```
