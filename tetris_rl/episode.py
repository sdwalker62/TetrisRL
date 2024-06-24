r"""Episode logic for a terminal-based Tetris game. Adapted heavily from https://github.com/shkolovy/tetris-terminal/tree/master

All credit goes to the original author.
"""

import random
from dataclasses import dataclass

import numpy as np

from .tetromino import Tetromino

# Constants
N_ROWS = 20
N_COLS = 10


@dataclass
class EpisodeStatistics:
    score: int = 0
    lines_cleared: int = 0
    level: int = 1


class Episode:
    def __init__(self, mode: str = "bot"):
        # Game
        self.mode = mode
        # There are 5 tetrominos https://en.wikipedia.org/wiki/Tetromino
        self.tetromino_templates = {
            "T_BLOCK": np.array([[0, 1, 0], [1, 1, 1]]),
            "L_BLOCK": np.array([[1, 0], [1, 0], [1, 1]]),
            "S_BLOCK": np.array([[0, 1, 1], [1, 1, 0]]),
            "O_BLOCK": np.array([[1, 1], [1, 1]]),
            "I_BLOCK": np.array([[1], [1], [1], [1]]),
        }
        self.board = self._init_board()
        self.cur_tetromino = None
        self.next_tetromino = None
        self.cur_tetromino_pos = None
        self.episode_over = False
        self.episode_stats = EpisodeStatistics()

    def init_episode(self):
        r"""Initialize the game state."""
        self.board = self._init_board()
        self.cur_tetromino = None
        self.next_tetromino = None
        self.cur_tetromino_pos = None
        self.episode_over = False
        self.episode_stats = EpisodeStatistics()

    def get_episode_over_flag(self):
        return self.episode_over

    def _is_overlapping(self, pos, tetromino: Tetromino):
        r"""Check if the tetromino is overlapping with the board."""
        size = tetromino.size()
        for i in range(size[0]):
            for j in range(size[1]):
                if tetromino.shape[i][j] == 1:
                    if self.board[pos[0] + i][pos[1] + j] == 1:
                        return True
        return False

    def _is_move_legal(self, pos, tetromino: Tetromino):
        r"""Check if the move is legal."""

        # First check that the current position is within the board
        size = tetromino.size()
        if pos[1] < 0 or pos[1] + size[1] > N_ROWS or pos[0] + size[0] > N_COLS:
            return False

        return not self._is_overlapping(pos, tetromino)

    def rotate_tetromino(self):
        r"""Rotate the current tetromino."""
        self.cur_tetromino = np.rot90(self.cur_tetromino)

    def move_tetromino(self, direction):
        r"""Attempt to move the current tetromino."""
        pos = self.cur_tetromino_pos
        match direction:
            case "left":
                new_pos = (pos[0], pos[1] - 1)
            case "right":
                new_pos = (pos[0], pos[1] + 1)
            case "down":
                new_pos = (pos[0] + 1, pos[1])
            case _:  # Invalid direction
                raise ValueError(f"Invalid direction: {direction}")

        if self._is_move_legal(new_pos, self.cur_tetromino.shape):
            self.cur_tetromino_pos = new_pos
        elif direction == "down":
            self._land_tetromino()
            self._clear_lines()
            self._spawn_tetromino()

    def _land_tetromino(self):
        r"""Land the current tetromino."""
        size = self.cur_tetromino.size()
        for i in range(size[0]):
            for j in range(size[1]):
                if self.cur_tetromino.shape[i][j] == 1:
                    self.board[self.cur_tetromino_pos[0] + i][
                        self.cur_tetromino_pos[1] + j
                    ] = 1

    def _clear_lines(self):
        r"""Clear any lines that are full."""
        for i in range(N_ROWS):
            if all(col != 0 for col in self.board[i]):
                for j in range(i, 0, -1):
                    self.board[j] = self.board[j - 1]
                self.board[0] = np.zeros(N_COLS)
                self.episode_stats.lines_cleared += 1
                if self.episode_stats.lines_cleared % 10 == 0:
                    self.episode_stats.level += 1

    def hard_drop(self):
        r"""Hard drop the current tetromino."""
        i = 1
        while self._is_move_legal(
            (self.cur_tetromino_pos[0] + i, self.cur_tetromino_pos[1]),
            self.cur_tetromino.shape,
        ):
            i += 1
            self.move_tetromino("down")
        self._land_tetromino()
        self._clear_lines()
        self._spawn_tetromino()

    def _spawn_tetromino(self):
        r"""Spawn a new tetromino."""
        if self.cur_tetromino is None:
            self.cur_tetromino = self._get_new_teromino()
            self.next_tetromino = self._get_new_teromino()
        else:
            self.cur_tetromino = self.next_tetromino
            self.next_tetromino = self._get_new_teromino()

        size = self.cur_tetromino.size()
        col_pos = (0, int(N_COLS / 2 - size[1] / 2))
        self.cur_tetromino_pos = [0, col_pos]

        if self._is_overlapping(self.cur_tetromino_pos, self.cur_tetromino.shape):
            self.episode_over = True
        else:
            self.episode_stats.score += 1

    def _get_new_teromino(self):
        r"""Get a new tetromino."""
        type = np.random.choice(self.tetromino_templates.keys())
        tetromino = Tetromino(type)

        if random.getrandbits(1):
            tetromino.flip()

        return tetromino

    @staticmethod
    def _init_board():
        r"""Initialize with all zeroes."""
        return np.zeros((N_ROWS, N_COLS))

    def generate_random_board(self):
        return np.random.randint(0, 2, (10, 20))
