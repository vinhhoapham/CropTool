from PIL import Image
import numpy as np


class Resolution():
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def generate_empty_numpy_array(self):
        return np.full((self.height, self.width), None)

    def generate_empty_image(self, mode='L'):
        return Image.new(mode, (self.width, self.height))

    def is_in_resolution(self, coordinate):
        row, col = coordinate.get_tuple()
        return 0 <= row < self.height and 0 <= col < self.width
