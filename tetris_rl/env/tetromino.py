import numpy as np


class Tetromino:
    positions = []
    current_position = 0

    def __init__(self, type: str):
        match type:
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
        self.current_position = (self.current_position + 1) % len(self.positions)
        return self._get_representation()

    def rotate_counter_clockwise(self) -> np.ndarray:
        self.current_position = (self.current_position - 1) % len(self.positions)
        return self._get_representation()

    def _get_representation(self) -> np.ndarray:
        return self.positions[self.current_position]

    def spawn(self) -> np.ndarray:
        self.current_position = 0
        return self.positions[0]


class ITetromino(Tetromino):
    tetromino_idx = 1
    left_action_oob = [0, 2, 0, 1]
    right_action_oob = [3, 2, 3, 1]
    positions = [
        np.array([[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]),
        np.array([[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]),
        np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]),
        np.array([[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]),
    ]


class JTetromino(Tetromino):
    tetromino_idx = 2
    left_action_oob = [0, 1, 0, 0]
    right_action_oob = [2, 2, 2, 1]
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
    tetromino_idx = 3
    left_action_oob = [0, 1, 0, 0]
    right_action_oob = [2, 2, 2, 1]
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
    tetromino_idx = 4
    left_action_oob = [1, 1, 1, 1]
    right_action_oob = [2, 2, 2, 2]
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
    tetromino_idx = 5
    left_action_oob = [0, 1, 0, 0]
    right_action_oob = [2, 2, 2, 1]
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
    tetromino_idx = 6
    left_action_oob = [0, 1, 0, 0]
    right_action_oob = [2, 2, 2, 1]
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
    tetromino_idx = 7
    left_action_oob = [0, 1, 0, 0]
    right_action_oob = [2, 2, 2, 1]
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
