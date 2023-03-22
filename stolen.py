import math
import os.path

from PIL import Image, ImageDraw



class ConvertToCarthesian:
    """
    Represents an image on which to draw

    The center of the image is considered (0, 0). The corners are (-1, 1), (1, 1), (1, -1) and (-1, -1)
    """

    # TODO: Use this Canvas in Pointillizer


    def __init__(self, size = (800,800)):
        self.width, self.height = size

    def give_circle_coords(self, pos, r: int, color):
        x, y = pos
        left = self._rel_x_to_abs_x(x) - r
        right = self._rel_x_to_abs_x(x) + r
        upper = self._rel_y_to_abs_y(y) - r
        lower = self._rel_y_to_abs_y(y) + r
        return left,upper,right,lower

    def coord_to_coord_on_canvas(self, coord):
        x, y = coord
        return self._rel_x_to_abs_x(x), self._rel_y_to_abs_y(y)

    def _rel_x_to_abs_x(self, x):
        abs_x = int((1 + x) * self.width / 2)

        # Constrain to canvas
        if abs_x < 0:
            abs_x = 0
        if abs_x >= self.width:
            abs_x = self.width - 1

        return abs_x

    def _rel_y_to_abs_y(self, y):
        abs_y = int((1 + y) * self.height / 2)

        # Constrain to canvas
        if abs_y < 0:
            abs_y = 0
        if abs_y >= self.height:
            abs_y = self.height - 1

        return abs_y