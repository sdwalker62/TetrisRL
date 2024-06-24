r"""
For more information visit
https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/

All rules used in the environment are based on the Tetris guidelines posted at:

https://tetris.wiki/Tetris_Guideline
"""

import numpy as np
from gymnasium import Env, spaces


class TetrisEnv(Env):
    r"""Implements the Tetris environment for OpenAI Gym."""

    metadata = {"render_modes": ["web_viewer"], "render_fps": 60}
    playfield_width = 10  # Number of columns in the playfield
    visual_height = 20  # Number of rows visible to the player
    buffer_height = 20  # Number of rows offscreen for spawning and rotating tetrminos

    def __init__(self, render_mode=None):
        # TODO: Complete the implementation of these params
        """
        Actions = {
            left,
            right,
            soft-drop,
            hard-drop,
            counter-clockwise rotations,
            clockwise rotations
        }
        """
        self.action_space = spaces.Discrete(6)
        """
        Observation space is a 10x20 grid with 6 possible values for each cell:
            0: empty,
            1: I,
            2: O,
            3: T,
            4: L,
            5: S,
        """
        self.observation_space = spaces.MultiDiscrete(
            np.full((self.playfield_width, self.visual_height), 5)
        )
        self.reward_range = None
        self.spec = None
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.playfield = self._init_playfield()
        self.bag = []  # The next seven tetrominos to be played, gets refilled when empty

    def step(self, action):
        r"""Take a single step in the environment."""
        pass

    def _check_if_oob(self):
        r"""Check if the current tetromino in play is out of bounds."""
        pass

    def _check_if_collision(self):
        r"""Checks if the current tetromino in play has collided with any static tetrominos."""
        pass

    def _check_if_game_over(self):
        r"""Checks if a terminal condition has been met.

        In Tetris the following conditions will terminate the episode:
            1. A piece is spawned overlapping at least one block in the playfield.
            2. A piece locks completely above the visible portion of the playfield.
            3. A piece is pished above the 20-row buffer zone.
        """
        pass

    def _init_playfield(self) -> np.ndarray:
        r"""Creates a default playfield with no tetrominos."""
        return np.zeros((self.playfield_width, self.visual_height + self.buffer_height))

    def _refill_bag(self) -> list:
        r"""Populates the bag with a random ordering of the seven tetrominos. All seven tetrominos are included in the bag."""
        pass

    def reset(self, seed=None, options=None, **kwargs):
        r"""Resets the environment to its initial state."""
        pass

    def render(self) -> np.ndarray:
        r"""Render a single frame for the frontend"""
        pass

    def close(self):
        r"""Closing logic for the environment."""
        pass
