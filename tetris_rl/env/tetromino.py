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

    def rotate_clockwise(self) -> np.ndarray:
        r"""Rotate the tetromino by incrementing the position index."""
        self.current_position = (self.current_position + 1) % len(self.positions)
        return self.get_representation()

    def rotate_counter_clockwise(self) -> np.ndarray:
        r"""Rotate the tetromino by decrementing the position index."""
        self.current_position = (self.current_position - 1) % len(self.positions)
        return self.get_representation()

    def get_representation(self) -> np.ndarray:
        r"""Use the np.ndarray for collision detections and rendering."""
        return self.trim(self.trim(self.positions[self.current_position]))

    def spawn(self) -> np.ndarray:
        r"""Spawn with default values."""
        self.current_position = 0
        r = self.trim(self.positions[0])
        self.height = r.shape[0]
        self.width = r.shape[1]
        print(f"Spawned {self.type} tetromino with shape {r.shape}.")
        return self.positions[0]

    def trim(self, x: np.ndarray) -> np.ndarray:
        r"""Trim the tetromino to its minimal bounding box."""
        x = x[1:] if x[0, :].sum() == 0 else x  # trim first row
        x = x[:-1] if x[-1, :].sum() == 0 else x  # trim last row
        x = x[:, 1:] if x[:, 0].sum() == 0 else x  # trim first column
        x = x[:, :-1] if x[:, -1].sum() == 0 else x  # trim last column
        return x


class ITetromino(Tetromino):
    r"""I-shaped tetromino."""

    tetromino_idx = 1
    first_non_zero_col_per_idx = [0, 2, 0, 1]
    last_non_zero_col_per_idx = [3, 2, 3, 1]
    first_non_zero_row_per_idx = [1, 0, 2, 0]
    last_non_zero_row_per_idx = [1, 3, 2, 3]
    positions = [
        np.array([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]),
        np.array([[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]),
        np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]),
        np.array([[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]),
    ]


class JTetromino(Tetromino):
    r"""J-shaped tetromino."""

    tetromino_idx = 2
    first_non_zero_col_per_idx = [0, 1, 0, 0]
    last_non_zero_col_per_idx = [2, 2, 2, 1]
    first_non_zero_row_per_idx = [0, 0, 1, 0]
    last_non_zero_row_per_idx = [1, 2, 2, 2]
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
    first_non_zero_col_per_idx = [0, 1, 0, 0]
    last_non_zero_col_per_idx = [2, 2, 2, 1]
    first_non_zero_row_per_idx = [0, 0, 1, 0]
    last_non_zero_row_per_idx = [1, 2, 2, 2]
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
    first_non_zero_col_per_idx = [1, 1, 1, 1]
    last_non_zero_col_per_idx = [2, 2, 2, 2]
    first_non_zero_row_per_idx = [0, 0, 0, 0]
    last_non_zero_row_per_idx = [1, 1, 1, 1]
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
    first_non_zero_col_per_idx = [0, 1, 0, 0]
    last_non_zero_col_per_idx = [2, 2, 2, 1]
    first_non_zero_row_per_idx = [0, 0, 1, 0]
    last_non_zero_row_per_idx = [1, 2, 2, 2]
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
    first_non_zero_col_per_idx = [0, 1, 0, 0]
    last_non_zero_col_per_idx = [2, 2, 2, 1]
    first_non_zero_row_per_idx = [0, 0, 1, 0]
    last_non_zero_row_per_idx = [1, 2, 2, 2]
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
    first_non_zero_col_per_idx = [0, 1, 0, 0]
    last_non_zero_col_per_idx = [2, 2, 2, 1]
    first_non_zero_row_per_idx = [0, 0, 1, 0]
    last_non_zero_row_per_idx = [1, 2, 2, 2]
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
