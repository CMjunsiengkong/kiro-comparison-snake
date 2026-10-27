from snake_game import config


def test_grid_dimensions():
    assert (config.GRID_WIDTH, config.GRID_HEIGHT) == (20, 20)


def test_cell_size():
    assert config.CELL_SIZE == 30


def test_window_size():
    assert (config.WINDOW_WIDTH, config.WINDOW_HEIGHT) == (600, 600)
    assert config.WINDOW_WIDTH == config.GRID_WIDTH * config.CELL_SIZE
    assert config.WINDOW_HEIGHT == config.GRID_HEIGHT * config.CELL_SIZE


def test_ticks_per_second():
    assert config.TICKS_PER_SECOND == 10


def test_window_title():
    assert config.WINDOW_TITLE == "Snake"
