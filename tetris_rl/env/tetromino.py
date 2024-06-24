import numpy as np


class Tetromino:
    positions = []
    current_position = 0

    def __init__(self):
        pass

    def rotate_clockwise(self) -> np.ndarray:
        self.current_position += 1
        return self._get_representation()

    def rotate_counter_clockwise(self) -> np.ndarray:
        self.current_position -= 1
        return self._get_representation()

    def _get_representation(self) -> np.ndarray:
        return self.positions[self.current_position]

    def spawn(self) -> np.ndarray:
        self.current_position = 0
        return self.positions[0]


class ITetromino(Tetromino):
    positions = [
        np.array([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]),
        np.array([[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]),
        np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]),
        np.array([[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]),
    ]


class JTetromino(Tetromino):
    positions = [
        np.array(
            [
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 0],
            ]
        ),
        np.array(
            [
                [0, 1, 1],
                [0, 1, 0],
                [0, 1, 0],
            ]
        ),
        np.array(
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 0, 1],
            ]
        ),
        np.array(
            [
                [0, 1, 0],
                [0, 1, 0],
                [1, 1, 0],
            ]
        ),
    ]


class LTetromino(Tetromino):
    positions = [
        np.array(
            [
                [0, 0, 1],
                [1, 1, 1],
                [0, 0, 0],
            ]
        ),
        np.array(
            [
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 1],
            ]
        ),
        np.array(
            [
                [0, 0, 0],
                [1, 1, 1],
                [1, 0, 0],
            ]
        ),
        np.array(
            [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 0],
            ]
        ),
    ]


class OTetromino(Tetromino):
    positions = [
        np.array(
            [
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
            ]
        ),
        np.array(
            [
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
            ]
        ),
        np.array(
            [
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
            ]
        ),
        np.array(
            [
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
            ]
        ),
    ]


class STetromino(Tetromino):
    positions = [
        np.array(
            [
                [0, 1, 1],
                [1, 1, 0],
                [0, 0, 0],
            ]
        ),
        np.array(
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 0, 1],
            ]
        ),
        np.array(
            [
                [0, 0, 0],
                [0, 1, 1],
                [1, 1, 0],
            ]
        ),
        np.array(
            [
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0],
            ]
        ),
    ]


class TTetromino(Tetromino):
    positions = [
        np.array(
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 0, 0],
            ]
        ),
        np.array(
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 1, 0],
            ]
        ),
        np.array(
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 1, 0],
            ]
        ),
        np.array(
            [
                [0, 1, 0],
                [1, 1, 0],
                [0, 1, 0],
            ]
        ),
    ]


class ZTetromino(Tetromino):
    positions = [
        np.array(
            [
                [1, 1, 0],
                [0, 1, 1],
                [0, 0, 0],
            ]
        ),
        np.array(
            [
                [0, 0, 1],
                [0, 1, 1],
                [0, 1, 0],
            ]
        ),
        np.array(
            [
                [0, 0, 0],
                [1, 1, 0],
                [0, 1, 1],
            ]
        ),
        np.array(
            [
                [0, 1, 0],
                [1, 1, 0],
                [1, 0, 0],
            ]
        ),
    ]
