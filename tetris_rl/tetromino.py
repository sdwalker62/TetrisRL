import numpy as np


class Tetromino:
    def __init__(self, tetromino_type):
        self.shape = self.tetromino_templates[tetromino_type]
        self.color = self.tetromino_colors[tetromino_type]

    def flip(self):
        self.shape = np.rot90(self.shape, 2)

    def size(self):
        return list(self.shape.shape)
