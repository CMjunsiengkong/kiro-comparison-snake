"""Hidden M3 acceptance tests. The agent never sees these; verify.sh adds them.

They cover only the interface stated in prompts/m3-feature.md. Every choice the
prompt leaves open (see decision-points.md) is deliberately not tested.
"""
from snake_game import config
from snake_game.highscore import load_high_score, save_high_score
from snake_game.logic import speed_for_score

# The highest possible score: the board is full, minus the 3 starting cells.
MAX_SCORE = config.GRID_WIDTH * config.GRID_HEIGHT - 3


def test_no_high_score_yet_is_zero(tmp_path):
    assert load_high_score(tmp_path / "highscore") == 0


def test_saved_high_score_loads_back(tmp_path):
    path = tmp_path / "highscore"
    save_high_score(path, 7)
    score = load_high_score(path)
    assert score == 7
    assert isinstance(score, int)


def test_higher_score_replaces_saved_one(tmp_path):
    path = tmp_path / "highscore"
    save_high_score(path, 7)
    save_high_score(path, 12)
    assert load_high_score(path) == 12


def test_speed_at_score_zero_is_todays_speed():
    assert speed_for_score(0) == config.TICKS_PER_SECOND


def test_speed_never_goes_down_as_score_grows():
    speeds = [speed_for_score(score) for score in range(MAX_SCORE + 1)]
    assert all(later >= earlier for earlier, later in zip(speeds, speeds[1:]))


def test_game_gets_faster_at_some_point():
    assert speed_for_score(MAX_SCORE) > config.TICKS_PER_SECOND
