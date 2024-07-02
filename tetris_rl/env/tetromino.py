r"""Tetromino classes for Tetris game."""

import numpy as np


class Tetromino:
    r"""Tetromino superclass."""

    positions = []
    current_position = 0
    existence_time = 0
    is_oob = False
    is_colliding = False
    height = 0
    width = 0

    # x and y represents the trimmed coordinates while hidden_x and hidden_y are the
    # non-trimmed coordinates used for rotations and other mechanics
    #
    # For example, for the J tetromino we have the following reprsentation:
    #
    #             (x, hidden_x)
    #                   V
    #  (y, hidden_y) > [1, 0, 0]
    #                  [1, 1, 1]
    #                  [0, 0, 0]
    #
    # Upon rotation we need to adjust the

    x, hidden_x = 0, 0
    y, hidden_y = 0, 0
    arr = None

    def __init__(self, tetromino_type: str):
        r"""Initialize one of the subclasses."""
        match tetromino_type:
            case "I":
                self.__class__ = ITetromino
                self.type = "I"
            case "J":
                self.__class__ = JTetromino
                self.type = "J"
            case "L":
                self.__class__ = LTetromino
                self.type = "L"
            case "O":
                self.__class__ = OTetromino
                self.type = "O"
            case "S":
                self.__class__ = STetromino
                self.type = "S"
            case "T":
                self.__class__ = TTetromino
                self.type = "T"
            case "Z":
                self.__class__ = ZTetromino
                self.type = "Z"
            case _:
                raise ValueError(f"Invalid tetromino type: {type}")
        self.arr = self.positions[0]

    def rotate_clockwise(self) -> np.ndarray:
        r"""Rotate the tetromino by incrementing the position index."""
        self.current_position = (self.current_position + 1) % len(self.positions)
        self.arr = self.positions[self.current_position]

    def rotate_counter_clockwise(self) -> np.ndarray:
        r"""Rotate the tetromino by decrementing the position index."""
        self.current_position = (self.current_position - 1) % len(self.positions)
        self.arr = self.positions[self.current_position]

    # def get_representation(self) -> np.ndarray:
    #     r"""Use the np.ndarray for collision detections and rendering."""
    #     return self.positions[self.current_position]

    def spawn(self) -> np.ndarray:
        r"""Spawn with default values."""
        self.current_position = 0
        self.arr = self.trim(self.positions[0])
        self.height = self.arr.shape[0]
        self.width = self.arr.shape[1]
        print(f"Spawned {self.type} tetromino with shape {self.arr.shape}.")
        return self.positions[0]

    def trim(self, x: np.ndarray) -> np.ndarray:
        r"""Trim the tetromino to its minimal bounding box."""
        for _ in range(2):
            x = x[1:] if x[0, :].sum() == 0 else x  # trim first row
            x = x[:-1] if x[-1, :].sum() == 0 else x  # trim last row
            x = x[:, 1:] if x[:, 0].sum() == 0 else x  # trim first column
            x = x[:, :-1] if x[:, -1].sum() == 0 else x  # trim last column

        # # calculuate how many of the beginning rows and columns are empty
        # n_rows_empty, idx = 0, 0
        # while np.sum(x[idx, :]) == 0:
        #     n_rows_empty += 1
        #     idx += 1
        #     if idx == x.shape[0]:
        #         break

        # n_cols_empty, idx = 0, 0
        # while np.sum(x[:, idx]) == 0:
        #     n_cols_empty += 1
        #     idx += 1
        #     if idx == x.shape[1]:
        #         break

        # self.trimmed_x = self.non_trimmed_x + n_cols_empty
        # self.trimmed_y = self.non_trimmed_y + n_rows_empty

        return x

    def get_height(self) -> int:
        r"""Get the current tetromino height."""
        return self.arr.shape[0]

    def get_width(self) -> int:
        r"""Get the current tetromino width."""
        return self.arr.shape[1]

    def get_trimmed_height(self) -> int:
        r"""Get the current tetromino height without padding zeros."""
        return self.trim(self.arr).shape[0]

    def get_trimmed_width(self) -> int:
        r"""Get the current tetromino width without padding zeros."""
        return self.trim(self.arr).shape[1]


class ITetromino(Tetromino):
    r"""I-shaped tetromino."""

    tetromino_idx = 1
    positions = [
        np.array([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]),
        np.array([[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]),
        np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]),
        np.array([[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]),
    ]


class JTetromino(Tetromino):
    r"""J-shaped tetromino."""

    tetromino_idx = 2
    positions = [
        2
        * np.array(
            [
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 0],
            ],
        ),
        2
        * np.array(
            [
                [0, 1, 1],
                [0, 1, 0],
                [0, 1, 0],
            ],
        ),
        2
        * np.array(
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 0, 1],
            ],
        ),
        2
        * np.array(
            [
                [0, 1, 0],
                [0, 1, 0],
                [1, 1, 0],
            ],
        ),
    ]


class LTetromino(Tetromino):
    r"""L-shaped tetromino."""

    tetromino_idx = 3
    positions = [
        3
        * np.array(
            [
                [0, 0, 1],
                [1, 1, 1],
                [0, 0, 0],
            ],
        ),
        3
        * np.array(
            [
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 1],
            ],
        ),
        3
        * np.array(
            [
                [0, 0, 0],
                [1, 1, 1],
                [1, 0, 0],
            ],
        ),
        3
        * np.array(
            [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 0],
            ],
        ),
    ]


class OTetromino(Tetromino):
    r"""O-shaped tetromino."""

    tetromino_idx = 4
    positions = [
        4
        * np.array(
            [
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
            ],
        ),
        4
        * np.array(
            [
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
            ],
        ),
        4
        * np.array(
            [
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
            ],
        ),
        4
        * np.array(
            [
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
            ],
        ),
    ]


class STetromino(Tetromino):
    r"""S-shaped tetromino."""

    tetromino_idx = 5
    positions = [
        5
        * np.array(
            [
                [0, 1, 1],
                [1, 1, 0],
                [0, 0, 0],
            ],
        ),
        5
        * np.array(
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 0, 1],
            ],
        ),
        5
        * np.array(
            [
                [0, 0, 0],
                [0, 1, 1],
                [1, 1, 0],
            ],
        ),
        5
        * np.array(
            [
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0],
            ],
        ),
    ]


class TTetromino(Tetromino):
    r"""T-shaped tetromino."""

    tetromino_idx = 6
    positions = [
        6
        * np.array(
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 0, 0],
            ],
        ),
        6
        * np.array(
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 1, 0],
            ],
        ),
        6
        * np.array(
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 1, 0],
            ],
        ),
        6
        * np.array(
            [
                [0, 1, 0],
                [1, 1, 0],
                [0, 1, 0],
            ],
        ),
    ]


class ZTetromino(Tetromino):
    r"""Z-shaped tetromino."""

    tetromino_idx = 7
    positions = [
        7
        * np.array(
            [
                [1, 1, 0],
                [0, 1, 1],
                [0, 0, 0],
            ],
        ),
        7
        * np.array(
            [
                [0, 0, 1],
                [0, 1, 1],
                [0, 1, 0],
            ],
        ),
        7
        * np.array(
            [
                [0, 0, 0],
                [1, 1, 0],
                [0, 1, 1],
            ],
        ),
        7
        * np.array(
            [
                [0, 1, 0],
                [1, 1, 0],
                [1, 0, 0],
            ],
        ),
    ]
