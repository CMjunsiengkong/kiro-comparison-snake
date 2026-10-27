"""Game constants: grid size, speed, window, and colors."""
from __future__ import annotations

GRID_WIDTH = 20
GRID_HEIGHT = 20
CELL_SIZE = 30
TICKS_PER_SECOND = 10
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE  # 600
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE  # 600
WINDOW_TITLE = "Snake"

# RGB colors
BACKGROUND_COLOR = (20, 20, 20)
GRID_COLOR = (35, 35, 35)
SNAKE_HEAD_COLOR = (120, 230, 120)
SNAKE_BODY_COLOR = (40, 170, 60)
FOOD_COLOR = (220, 50, 50)
TEXT_COLOR = (240, 240, 240)
OVERLAY_COLOR = (0, 0, 0, 170)  # RGBA: semi-transparent black
