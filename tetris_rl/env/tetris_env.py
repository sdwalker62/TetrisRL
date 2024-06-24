r"""
For more information visit
https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/
"""

import numpy as np
from gymnasium import Env, spaces


class TetrisEnv(Env):
    r"""Implements the Tetris environment for OpenAI Gym."""

    metadata = {"render_modes": ["web_viewer"], "render_fps": 60}

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
        self.observation_space = spaces.MultiDiscrete(np.full((10, 20), 5))
        self.reward_range = None
        self.spec = None
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def step(self, action):
        pass

    def reset(self, seed=None, options=None, **kwargs):
        pass

    def render(self) -> np.ndarray:
        pass

    def close(self):
        pass
