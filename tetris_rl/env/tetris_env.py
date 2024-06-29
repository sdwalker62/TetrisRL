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

    def step(self, action) -> tuple[np.ndarray, float, bool, bool, dict]:
        """Take a single step of the environment.

        Actions every step
        ------------------
        Note: Steps should align with the tick rate of the game!

        1. [ ] Retrieve current_level and calculate gravity, store gravity value
            a. Every step may not apply gravity, check the stored gravity value
            b. Compare the stored gravity value with the step number
            c. Move down when step mod gravity rate == 0
        2. [ ] Calculate proposed position from action
            a. Check if the proposed move causes a collision
                i. If the action is a rotation, check for wall kicks (optional)
                ii. If the collision is below, the piece has landed
            b. If it is a left or right move, check if it is out of bounds
                i. If it is out of bounds, do not move the piece
            c. Check if the piece has landed on the ground
        3. [ ] Update the position of the current piece with the proposed
        4. [ ] Check for line clears
        5. [ ] Check for game over
        6. [ ] Spawn a new piece
        7. [ ] Calculate score
        8. [ ] Calculate level
            a. Update gravity
        9. [ ] Update linesCleared
        10. [ ] Stream statistics to the frontend
        11. [ ] Render the playfield

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

        # From looking at the online tetris, there is always a gravity applied
        # to the piece even if you move it, so moving it left and right
        # still cause it to go down after awhile, yet you can get a few
        # left and right moves in before the piece goes down.

        # Check if OOB
        # Check for collisions
        # If rotating, check for wall kicks
        # Check for landing
        #   Check for game over
        #   If landed, check for line clears
        #       If landed, update statistics
        #   Spawn new piece

        is_oob, is_colliding = False, False
        proposed_pos = self._move(action)

        # Cases:
        # 1. Proposed move would cause the tetromino to go OOB
        # 2. Proposed move would cause the tetromino to collide
        # 3. Proposed move would cause the tetromino to land

        # Case 1: OOB
        is_oob = self._check_if_oob(proposed_pos, action)

        # Case 2: Collision
        if not is_oob:
            is_colliding = self._check_if_collision(proposed_pos)

        # Case 3: Landing
        if not is_colliding and self._check_if_landed(proposed_pos):
            self.playfield += self.ghost_playfield
            self._handle_step_end(True)
            return self.playfield, 0, False, False, {}

        # Action down would cause the piece to collide with another
        if is_colliding and action == 2:
            print("Colliding")
            self._update_ghost((self.cur_tetromino.x, self.cur_tetromino.y))
            self.playfield += self.ghost_playfield
            self._handle_step_end(True)
            return self.playfield, 0, False, False, {}

        if not is_oob and not is_colliding:
            self._perform_move(proposed_pos)
            self._handle_step_end()

        return self.playfield, 0, False, False, {}

    def _handle_step_end(self, should_spawn_next_piece: bool = False):
        r"""Handle the end of a step in the environment."""
        is_game_over = False
        if not is_game_over and should_spawn_next_piece:
            # Check if the bag needs refilling
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
                return self.cur_tetromino.x, self.cur_tetromino.y + 1
            case 5:  # counter-clockwise rotation
                self.cur_tetromino.rotate_counter_clockwise()
                return self.cur_tetromino.x, self.cur_tetromino.y + 1
            case _:
                return self.cur_tetromino.x, self.cur_tetromino.y + 1

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

    def _check_if_landed(self, proposed_move: tuple[int]) -> bool:
        r"""Check if the current tetromino in play has landed on the playfield."""
        bottom = proposed_move[1] + self.cur_tetromino.height
        if bottom > self.visual_height + self.buffer_height:
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
            (self.visual_height + self.buffer_height, self.playfield_width)
        )
        r = self.cur_tetromino.get_representation()
        x, y = proposed_pos[0], proposed_pos[1]
        try:
            collision_mask[y : y + r.shape[0], x : x + r.shape[1]] += r
        except ValueError as e:
            print(e)
            print(f"y: {y}, x: {x}")
            print(r.shape)
            print(f"rows_start: {y}, rows_end: {y + r.shape[0]}")
            print(f"cols_start: {x}, cols_end: {x + r.shape[1]}")
            print(f"proposed_pos: {proposed_pos}")
            print(f"playfield shape: {self.playfield.shape}")
            print(collision_mask)
            exit()
        return np.any(np.logical_and(self.ghost_playfield > 0, self.playfield > 0))

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
        r = self.cur_tetromino.get_representation()
        self.cur_tetromino.height = r.shape[0]
        self.cur_tetromino.width = r.shape[1]
        # Create the ghost that we will use for collision detection
        self.ghost_playfield = self._create_new_ghost_playfield()
        self.ghost_playfield[
            self.cur_tetromino.y : self.cur_tetromino.y + r.shape[0],
            self.cur_tetromino.x : self.cur_tetromino.x + r.shape[1],
        ] += r

    def _create_new_ghost_playfield(self):
        return np.zeros((self.visual_height + self.buffer_height, self.playfield_width))

    def _update_ghost(self, proposed_pos: tuple[int]):
        r"""Update the ghost piece to reflect the current position of the active piece."""
        r = self.cur_tetromino.get_representation()
        x, y = proposed_pos[0], proposed_pos[1]
        self.ghost_playfield = self._create_new_ghost_playfield()
        self.ghost_playfield[y : y + r.shape[0], x : x + r.shape[1]] += r

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
        r = self.cur_tetromino.get_representation()
        arr = self.playfield.copy()
        arr[
            self.cur_tetromino.y : self.cur_tetromino.y + r.shape[0],
            self.cur_tetromino.x : self.cur_tetromino.x + r.shape[1],
        ] += r
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
                {"representation": self.bag[0].get_representation().tolist()},
            ),
            headers={"Content-Type": "application/json"},
            timeout=TIME_OUT,
        )

    def close(self):
        r"""Close open connections before closing the environment."""
        print("Closing Tetris environment")
