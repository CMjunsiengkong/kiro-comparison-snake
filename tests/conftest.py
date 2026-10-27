"""Shared pytest setup.

Use SDL's dummy drivers so rendering tests run headless (no window, no audio).
This must happen before pygame initialises its display or mixer.
"""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
