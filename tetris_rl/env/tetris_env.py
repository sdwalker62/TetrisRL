r"""
For more information visit
https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/

All rules used in the environment are based on the Tetris guidelines posted at:

https://tetris.wiki/Tetris_Guideline
"""

import json
import random
import time

import numpy as np
import requests
from gymnasium import Env, spaces

from tetris_rl.env.tetromino import Tetromino

FPS = 60


class TetrisEnv(Env):
    r"""Implements the Tetris environment for OpenAI Gym."""

    metadata = {"render_modes": ["web_viewer"], "render_fps": 60}
    playfield_width = 10  # Number of columns in the playfield
    visual_height = 20  # Number of rows visible to the player
    buffer_height = 20  # Number of rows offscreen for spawning and rotating tetrminos
    tetromino_ids = ["I", "J", "L", "O", "S", "T", "Z"]

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
        """
        All positions are referenced from the top-left corner of the np.array representing the piece.
        """
        self.cur_tetromino_pos = None
        self.next_tetromino_pos = None
        self.cur_tetromino = None
        self.bag = (
            self._refill_bag()
        )  # The next seven tetrominos to be played, gets refilled when empty
        """
        This piece will be used to test for collisions. An empty playfield will be created consisting of all
        zeroes except where the proposed tetromino will be placed. This will be used to test for collisions
        by creating a mask and if any values are non-zero it will indicate a collision.
        """
        self.ghost_playfield = np.zeros(
            (self.visual_height + self.buffer_height, self.playfield_width)
        )

    def step(self, action):
        r"""Take a single step in the environment."""

        # next_pos = self._move(action)

        # if self._check_if_oob(next_pos):
        #     next_pos = self.cur_tetromino_pos

        # Check if OOB
        # Check for collisions
        # If rotating, check for wall kicks
        # Check for landing
        #   Check for game over
        #   If landed, check for line clears
        #       If landed, update statistics
        #   Spawn new piece

        if self.render_mode == "web_viewer":
            self.render()

        return self.playfield, 0, False, False, {}

    def _move(self, action):
        pass

    def _check_if_oob(self, move_left: bool):
        r"""Check if the current tetromino in play is out of bounds."""
        if move_left:
            left_edge = (
                self.cur_tetromino_pos[0]
                + self.cur_tetromino.left_action_oob[
                    self.cur_tetromino.current_position
                ]
            )
            return left_edge < 0
        else:
            right_edge = (
                self.cur_tetromino_pos[0]
                + self.cur_tetromino.right_action_oob[
                    self.cur_tetromino.current_position
                ]
            )
            return right_edge >= self.playfield_width

    def _check_if_landed(self):
        r"""Check if the current tetromino in play has landed on the playfield."""
        pass

    def _check_if_collision(self) -> bool:
        r"""Checks if the current tetromino in play has collided with any static tetrominos.

        This will also be used for wall kicks.

        The idea is simple, say we have two small boards where the 1 represents a block and 0 represents an empty space.

        board1 = [
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0]
        ]

        board2 = [
            [1, 1, 1],
            [0, 0, 0],
            [0, 0, 0]
        ]

        Then,

        board1 > 0 = [
            [True, False, False],
            [True, False, False],
            [True, False, False]
        ]

        board2 > 0 = [
            [True, True, True],
            [False, False, False],
            [False, False, False]
        ]

        Element-wise logical AND results in an array where the True values are the overlapping blocks.

        np.logical_and(board1 > 0, board2 > 0) = [
            [True, False, False],
            [False, False, False],
            [False, False, False]
        ]

        We then return the result of np.any() to check if there are any overlapping blocks in the array:

        np.any(np.logical_and(board1 > 0, board2 > 0)) = True

        """
        return np.any(np.logical_and(self.ghost_playfield > 0, self.playfield > 0))

    def _spawn_tetromino(self) -> None:
        r"""Spawn a new tetromino at the top of the playfield.

        All tetrominos spawn on rows 21 and 22 of the playfield as per the guidelines.
        """
        if len(self.bag) == 0:
            self.bag = self._refill_bag()
        next_tetromino = self.bag.pop(0)
        tetromino_type = next_tetromino.type

        match tetromino_type:
            case "I" | "O":
                self.cur_tetromino_pos = (21, 3)
            case "T" | "S" | "Z" | "J" | "L":
                self.cur_tetromino_pos = (20, 3)

        self.cur_tetromino = next_tetromino
        representation = self.cur_tetromino._get_representation()
        self.ghost_playfield = self._create_new_ghost_playfield()
        self.ghost_playfield[
            self.cur_tetromino_pos[0] : self.cur_tetromino_pos[0]
            + representation.shape[0],
            self.cur_tetromino_pos[1] : self.cur_tetromino_pos[1]
            + representation.shape[1],
        ] += self.cur_tetromino._get_representation() * self.cur_tetromino.tetromino_idx
        self.playfield[
            self.cur_tetromino_pos[0] : self.cur_tetromino_pos[0]
            + representation.shape[0],
            self.cur_tetromino_pos[1] : self.cur_tetromino_pos[1]
            + representation.shape[1],
        ] += self.cur_tetromino._get_representation() * self.cur_tetromino.tetromino_idx

    def _create_new_ghost_playfield(self):
        return np.zeros((self.visual_height + self.buffer_height, self.playfield_width))

    def _update_ghost(self, shift: tuple):
        r"""Update the ghost piece to reflect the current position of the active piece."""
        self.collision_ghost = np.roll(self.collision_ghost, shift)

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
        return np.zeros((self.visual_height + self.buffer_height, self.playfield_width))

    def _refill_bag(self) -> list:
        r"""Populates the bag with a random ordering of the seven tetrominos. All seven tetrominos are included in the bag."""
        ids = random.sample(self.tetromino_ids, len(self.tetromino_ids))
        return [Tetromino(id) for id in ids]

    def reset(self, seed=None, options=None, **kwargs):
        r"""Resets the environment to its initial state."""
        self._spawn_tetromino()
        return self.playfield, {}

    def render(self) -> np.ndarray:
        r"""Render a single frame for the frontend"""
        data = json.dumps({"board": self.playfield.tolist()})
        headers = {"Content-Type": "application/json"}
        time.sleep(1 / FPS)
        requests.post("http://localhost:8000/tetris/frame", data=data, headers=headers)

    def close(self):
        r"""Closing logic for the environment."""
        pass
