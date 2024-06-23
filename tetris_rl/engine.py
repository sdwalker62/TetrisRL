r"""Episode logic for a terminal-based Tetris game. Adapted heavily from https://github.com/shkolovy/tetris-terminal/tree/master

All credit goes to the original author.
"""

import curses
import random
import time
from dataclasses import dataclass

import numpy as np
from textual.app import App, ComposeResult
from textual.widgets import Static

from .tetromino import Tetromino

BOARD_WIDTH = 15
BOARD_HEIGHT = 25

GAME_WINDOW_WIDTH = 2 * BOARD_WIDTH + 2
GAME_WINDOW_HEIGHT = BOARD_HEIGHT + 2

HELP_WINDOW_WIDTH = 19
HELP_WINDOW_HEIGHT = 7

STATUS_WINDOW_HEIGHT = 12
STATUS_WINDOW_WIDTH = HELP_WINDOW_WIDTH

TITLE_HEIGHT = 6

LEFT_MARGIN = 3

TITLE_WIDTH = FOOTER_WIDTH = 50


def generate_game_string(game_state: np.ndarray) -> str:
    r"""Using Static objects is too slow when rendering. Instead, we will
    use a string of ASCII characters to represent the game state.
    """

    state = ""

    for i in range(game_state.shape[0]):
        if game_state[i] == 1:
            state += "\u25a0"
        else:
            state += "\u25a1"
    state += "\n"
    return state


class TetrisBoard(App):
    r"""Rendering logic for a standard Teris board."""

    CSS_PATH = "tetris_board.tcss"
    N_ROWS = 20
    N_COLS = 10

    def compose(self) -> ComposeResult:
        state = np.random.randint(0, 2, (10))
        game_state = generate_game_string(state)
        yield Static(game_state, shrink=True, classes="game_row")
        yield Static(game_state, shrink=True, classes="game_row")


def init_colors():
    """Init colors"""

    curses.init_pair(99, 8, curses.COLOR_BLACK)  # 1 - grey
    curses.init_pair(98, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(97, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(96, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(95, curses.COLOR_BLACK, curses.COLOR_WHITE)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, 13)  # 13 - pink
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)


@dataclass
class EpisodeStatistics:
    score: int = 0
    lines_cleared: int = 0
    level: int = 1


class Episode:
    def __init__(self, mode: str = "ai"):
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

        # Display
        self.window = curses.newwin(
            GAME_WINDOW_HEIGHT, GAME_WINDOW_WIDTH, TITLE_HEIGHT, LEFT_MARGIN
        )
        self.window.nodelay(True)
        self.window.keypad(1)

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
        if (
            pos[1] < 0
            or pos[1] + size[1] > BOARD_WIDTH
            or pos[0] + size[0] > BOARD_HEIGHT
        ):
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
        for i in range(BOARD_HEIGHT):
            if all(col != 0 for col in self.board[i]):
                for j in range(i, 0, -1):
                    self.board[j] = self.board[j - 1]
                self.board[0] = np.zeros(BOARD_WIDTH)
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
        col_pos = (0, int(BOARD_WIDTH / 2 - size[1] / 2))
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
        return np.zeros((BOARD_HEIGHT, BOARD_WIDTH))

    @staticmethod
    def draw_title():
        """Draw title"""
        window = curses.newwin(TITLE_HEIGHT, TITLE_WIDTH, 1, LEFT_MARGIN)
        window.addstr(
            0, 4, "#####  ####  #####  ###    #   ####", curses.color_pair(98)
        )
        window.addstr(1, 4, "  #    #       #    #  #      #", curses.color_pair(98))
        window.addstr(2, 4, "  #    ###     #    # #    #   ###", curses.color_pair(98))
        window.addstr(
            3, 4, "  #    #       #    #  #   #      #", curses.color_pair(98)
        )
        window.addstr(4, 4, "  #    ####    #    #   #  #  ####", curses.color_pair(98))

        window.addstr(2, 0, " *", curses.color_pair(97))
        window.addstr(2, 41, " *", curses.color_pair(97))

        window.refresh()

    @staticmethod
    def draw_footer():
        title = "Made with"
        window = curses.newwin(
            1, FOOTER_WIDTH, TITLE_HEIGHT + GAME_WINDOW_HEIGHT + 1, LEFT_MARGIN
        )
        col_pos = int((GAME_WINDOW_WIDTH + STATUS_WINDOW_WIDTH - len(title) + 1) / 2)
        window.addstr(0, col_pos, title, curses.color_pair(98))
        window.addstr(0, col_pos + len(title) + 1, "❤", curses.color_pair(97))

        window.refresh()

    def generate_random_board(self):
        return np.random.randint(0, 2, (10, 20))

    def draw_board(self):
        # self.window.border()
        board = self.generate_random_board()
        for a in range(board.shape[0]):
            for b in range(board.shape[1]):
                if board[a][b] == 1:
                    self.window.addstr(a + 1, b + 1, "B", curses.color_pair(97))
                else:
                    # draw net
                    self.window.addstr(a + 1, b + 1, "A", curses.color_pair(99))
        self.window.refresh()


if __name__ == "__main__":
    # If the game encounters an error we need to close the window or the terminal will be
    # unusable.
    try:
        scr = curses.initscr()
        curses.beep()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)

        init_colors()

        episode = Episode(mode="manual")

        episode.draw_title()
        episode.draw_footer()
        episode.draw_board()

        time.sleep(5)

    finally:
        curses.endwin()
        curses.endwin()
