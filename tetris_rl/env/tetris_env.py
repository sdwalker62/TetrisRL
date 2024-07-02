r"""Implements the Tetris environment for OpenAI Gym.

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

TIME_OUT = 10


class TetrisEnv(Env):  # pylint: disable=too-many-instance-attributes
    r"""Implements the Tetris environment for OpenAI Gym."""

    metadata = {"render_modes": ["web_viewer"], "render_fps": 7}
    playfield_width = 10  # Number of columns in the playfield
    visual_height = 20  # Number of rows visible to the player
    buffer_height = 20  # Number of rows offscreen for spawning and rotating tetrminos
    tetromino_ids = ["I", "J", "L", "O", "S", "T", "Z"]

    def __init__(
        self,
        render_mode: str = None,
        manual_play: bool = False,
    ) -> None:
        r"""Initialize the event loop and game logic."""
        self.manual_play = manual_play
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
            np.full((self.playfield_width, self.visual_height), 5),
        )
        self.reward_range = None
        self.spec = None
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.playfield = self._init_playfield()
        """
        All positions are referenced from the top-left corner of the np.array
        representing the piece.
        """
        self.cur_tetromino_pos = None
        self.next_tetromino_pos = None
        self.cur_tetromino = None
        self.bag = (
            self._refill_bag()
        )  # The next seven tetrominos to be played, gets refilled when empty
        """
        This piece will be used to test for collisions. An empty playfield will
        be created consisting of all zeroes except where the proposed tetromino
        will be placed. This will be used to test for collisions by creating a
        mask and if any values are non-zero it will indicate a collision.
        """
        self.ghost_playfield = np.zeros(
            (self.visual_height + self.buffer_height, self.playfield_width),
        )

        self.current_level = 0
        self.gravity = 0
        self.should_spawn_next_piece = False

    def step(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict]:
        """Take a single step of the environment.

        Parameters
        ----------
        action : int
            action id

        Returns
        -------
        tuple[np.ndarray, float, bool, bool, dict]:
            information about the current episode including the next state

        """
        self._update_gravity()
        proposed_pos = self._move(action)

        # Check conditions
        if self._check_if_valid_pos(proposed_pos, action):
            self._perform_move(proposed_pos)
            # Handle terminal conditions
            if self._check_terminal_conditions(proposed_pos):
                self.playfield += self.ghost_playfield
                self._handle_step_end(True)
                return self.playfield, 0, False, False, {}

            self._handle_step_end()

        return self.playfield, 0, False, False, {}

    def _check_terminal_conditions(self, proposed_pos: tuple[int]) -> bool:
        r"""Check if the episode is over."""
        return self._check_if_landed(proposed_pos) or self._is_on_another_tetromino()

    def _check_if_valid_pos(self, proposed_pos: tuple[int], action: int) -> bool:
        r"""Check if the proposed position is valid."""
        return not self._check_if_oob(
            proposed_pos,
            action,
        ) and not self._check_if_collision(proposed_pos)

    def _is_on_another_tetromino(self):
        r"""Check if the current tetromino is on top of another tetromino."""
        proposed_pos = self.cur_tetromino.x, self.cur_tetromino.y + 1
        return self._check_if_collision(proposed_pos)

    def _clear_lines(self):
        r"""Check for completed lines and clear them."""
        full_row_indices = np.where(np.all(self.playfield > 0, axis=1))[0].tolist()
        if len(full_row_indices) > 0:
            self.playfield = np.delete(self.playfield, full_row_indices, 0)
            for _ in range(len(full_row_indices)):
                self.playfield = np.insert(self.playfield, 0, 0, axis=0)

    def _handle_step_end(self, should_spawn_next_piece: bool = False):
        r"""Handle the end of a step in the environment."""
        # TODO: Check for game end
        is_game_over = False
        if not is_game_over:
            self._clear_lines()
            if should_spawn_next_piece:
                # Check if the bag needs refilling first
                if len(self.bag) == 1:
                    self.bag += self._refill_bag()
                self._spawn_tetromino()

        if self.render_mode == "web_viewer":
            self.render()

    def _perform_move(self, proposed_pos):
        r"""Update the playfield and ghost playfield."""
        self.cur_tetromino.x = proposed_pos[0]
        self.cur_tetromino.y = proposed_pos[1]
        self._update_ghost(proposed_pos)

    def _update_gravity(self):
        r"""Update the gravity value based on the current level.

        using the equation found here:

        https://harddrop.com/wiki/Tetris_Worlds
        """
        # time_spent_per_row = (0.8 - (self.current_level - 1) * 0.007) ** (
        #     self.current_level - 1
        # )

    def _move(self, action) -> tuple[int, int]:
        match action:
            case 0:  # left
                return self.cur_tetromino.x - 1, self.cur_tetromino.y
            case 1:  # right
                return self.cur_tetromino.x + 1, self.cur_tetromino.y
            case 2:  # soft-drop
                return self.cur_tetromino.x, self.cur_tetromino.y + 1
            case 3:  # hard-drop
                pass
            case 4:  # clockwise rotation
                self.cur_tetromino.rotate_clockwise()
                return self.cur_tetromino.x, self.cur_tetromino.y
            case 5:  # counter-clockwise rotation
                self.cur_tetromino.rotate_counter_clockwise()
                return self.cur_tetromino.x, self.cur_tetromino.y
            case _:
                return self.cur_tetromino.x, self.cur_tetromino.y

    def _check_if_oob(self, proposed_pos: tuple[int], action: int):
        r"""Check if the proposed tetromino position is out of bounds."""
        x, y = proposed_pos[0], proposed_pos[1]
        match action:
            case 0:  # left
                return x < 0
            case 1:  # right
                return x + self.cur_tetromino.width > self.playfield_width
            case 2:  # soft-drop
                return (
                    y + self.cur_tetromino.height
                    > self.visual_height + self.buffer_height
                )
            case _:
                return False

    def _check_if_landed(self, proposed_move: tuple[int]) -> bool:
        r"""Check if the current tetromino in play has landed on the playfield."""
        bottom = proposed_move[1] + self.cur_tetromino.height
        if bottom >= self.visual_height + self.buffer_height:
            return True
        return False

    def _check_if_collision(self, proposed_pos: tuple[int]) -> bool:
        r"""Check if the current tetromino is colliding.

        This will also be used for wall kicks.

        The idea is simple, say we have two small boards where the 1 represents
        a block and 0 represents an empty space.

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

        Element-wise logical AND results in an array where the True values are
        the overlapping blocks.

        np.logical_and(board1 > 0, board2 > 0) = [
            [True, False, False],
            [False, False, False],
            [False, False, False]
        ]

        We then return the result of np.any() to check if there are any
        overlapping blocks in the array:

        np.any(np.logical_and(board1 > 0, board2 > 0)) = True

        """
        # self.ghost_playfield = self._create_new_ghost_playfield()
        collision_mask = np.zeros(
            (self.visual_height + self.buffer_height, self.playfield_width),
        )
        _repr = self.cur_tetromino.arr
        x, y = proposed_pos[0], proposed_pos[1]
        try:
            collision_mask[y : y + _repr.shape[0], x : x + _repr.shape[1]] += _repr
        except ValueError as e:
            print("\n")
            print("#####################################################################")
            print(e)
            print("#####################################################################")
            print(f"Proposed position: y: {y}, x: {x}")
            print(f"Representation shape: {_repr.shape}")
            print(f"rows_start: {y}, rows_end: {y + _repr.shape[0]}")
            print(f"cols_start: {x}, cols_end: {x + _repr.shape[1]}")
            print(f"Playfield shape: {self.playfield.shape}")
            print("#####################################################################")
            print(collision_mask)
            print("\n")
            exit()
        return np.any(np.logical_and(collision_mask > 0, self.playfield > 0))

    def _spawn_tetromino(self) -> None:
        r"""Spawn a new tetromino at the top of the playfield.

        All tetrominos spawn on rows 21 and 22 of the playfield as per the
        guidelines.
        """
        # It should not be necessary to check for an empty bag since that is
        # done at the beginning of the environment step
        self.cur_tetromino = self.bag.pop(0)
        # remember that rows technically represent the y-axis not the x-axis
        self.cur_tetromino.x = 3
        self.cur_tetromino.y = 19 if self.cur_tetromino.type in ["I", "O"] else 19

        # grab the np.ndarray representation of the current piece
        _repr = self.cur_tetromino.arr
        self.cur_tetromino.height = _repr.shape[0]
        self.cur_tetromino.width = _repr.shape[1]
        # Create the ghost that we will use for collision detection
        self.ghost_playfield = self._create_new_ghost_playfield()
        self.ghost_playfield[
            self.cur_tetromino.y : self.cur_tetromino.y + _repr.shape[0],
            self.cur_tetromino.x : self.cur_tetromino.x + _repr.shape[1],
        ] += _repr

    def _create_new_ghost_playfield(self):
        return np.zeros((self.visual_height + self.buffer_height, self.playfield_width))

    def _update_ghost(self, proposed_pos: tuple[int]):
        r"""Update the ghost piece to reflect the current position of the active piece."""
        _repr = self.cur_tetromino.arr
        x, y = proposed_pos[0], proposed_pos[1]
        self.ghost_playfield = self._create_new_ghost_playfield()
        self.ghost_playfield[y : y + _repr.shape[0], x : x + _repr.shape[1]] += _repr

    def _check_if_game_over(self):
        r"""Check if a terminal condition has been met.

        In Tetris the following conditions will terminate the episode:
            1. A piece is spawned overlapping at least one block in the playfield.
            2. A piece locks completely above the visible portion of the playfield.
            3. A piece is pished above the 20-row buffer zone.
        """

    def _init_playfield(self) -> np.ndarray:
        r"""Create a default playfield with no tetrominos."""
        return np.zeros((self.visual_height + self.buffer_height, self.playfield_width))

    def _refill_bag(self) -> list:
        r"""Populate the bag with a random ordering of the seven tetrominos.

        Note: All seven tetrominos are included in the bag.
        """
        ids = random.sample(self.tetromino_ids, len(self.tetromino_ids))
        return [Tetromino(i) for i in ids]

    def reset(self):  # pylint: disable=arguments-differ
        r"""Reset the environment to its initial state."""
        self._spawn_tetromino()
        requests.post(
            "http://localhost:8000/tetris/mode",
            data=json.dumps({"mode": "human" if self.manual_play else "bot"}),
            headers={"Content-Type": "application/json"},
            timeout=TIME_OUT,
        )
        if self.manual_play:
            requests.post(
                "http://localhost:8000/tetris/clear_action_buffer",
                data=json.dumps({"should_clear": True}),
                headers={"Content-Type": "application/json"},
                timeout=TIME_OUT,
            )

        return self.playfield, {}

    def render(self) -> np.ndarray:
        r"""Render a single frame for the frontend."""
        _repr = self.cur_tetromino.arr
        arr = self.playfield.copy()
        arr[
            self.cur_tetromino.y : self.cur_tetromino.y + _repr.shape[0],
            self.cur_tetromino.x : self.cur_tetromino.x + _repr.shape[1],
        ] += _repr
        arr = arr[20:]  # only render the viewable portion of the playfield
        time.sleep(1 / self.metadata["render_fps"])
        requests.post(
            "http://localhost:8000/tetris/frame",
            data=json.dumps({"board": arr.tolist()}),
            headers={"Content-Type": "application/json"},
            timeout=TIME_OUT,
        )
        requests.post(
            "http://localhost:8000/tetris/stats",
            data=json.dumps(
                {
                    "score": 1,
                    "level": 2,
                    "lines_cleared": 3,
                },
            ),
            headers={"Content-Type": "application/json"},
            timeout=TIME_OUT,
        )
        requests.post(
            "http://localhost:8000/tetris/next_tetromino",
            data=json.dumps(
                {"representation": self.bag[0].arr.tolist()},
            ),
            headers={"Content-Type": "application/json"},
            timeout=TIME_OUT,
        )

    def close(self):
        r"""Close open connections before closing the environment."""
        print("Closing Tetris environment")
