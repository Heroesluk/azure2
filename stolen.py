import math
import os.path

from PIL import Image, ImageDraw



class Canvas:
    """
    Represents an image on which to draw

    The center of the image is considered (0, 0). The corners are (-1, 1), (1, 1), (1, -1) and (-1, -1)
    """

    # TODO: Use this Canvas in Pointillizer

    _common_dir = os.path.dirname(__file__)
    _src_dir = os.path.dirname(_common_dir)
    _root_dir = os.path.dirname(_src_dir)
    _img_dir = os.path.join(_root_dir, 'img')
    _input_dir = os.path.join(_img_dir, 'input')
    _output_dir = os.path.join(_img_dir, 'output')

    def __init__(self, image_name: str = None, size = None):
        assert image_name or size, 'You must provide a canvas Size when no image_name is provided'
        if image_name:
            self.img = Image.open(os.path.join(self._input_dir, image_name))
        else:
            self.img = Image.new(mode='RGB', size=size, color=(255, 255, 255))
        self.size = self.img.size
        self.width, self.height = self.size
        self.draw = ImageDraw.Draw(self.img)

    def draw_circle(self, pos, r: int, color):
        """
        Draw a circle at point (x,y) of radius r

        :param pos: Position of the center in relative coordinates (between -1 and 1)
        :param r: Radius of the circle in pixels on the canvas
        :param color: Color tuple of the circle
        """

        x, y = pos
        left = self._rel_x_to_abs_x(x) - r
        right = self._rel_x_to_abs_x(x) + r
        upper = self._rel_y_to_abs_y(y) - r
        lower = self._rel_y_to_abs_y(y) + r
        self.draw.ellipse((left, upper, right, lower), fill=color, outline=None)

    def draw_polygon(self, *points, color):
        abs_points = [(self.coord_to_coord_on_canvas(point)) for point in points]
        self.draw.polygon(abs_points, fill=color, outline=None)

    def draw_stroke(self, start, end, color, stroke_width=20):
        """
        Draw a stroke from start to end on the canvas

        A "stroke" is a line with rounded caps
        """

        dx = end[0] - start[0]
        dy = end[1] - start[1]
        phi = math.atan2(dy, dx)

        # TODO: Add visual to explain these expressions
        phi_1 = phi + math.pi / 2
        phi_2 = phi - math.pi / 2
        p1 = start[0] + stroke_width * math.cos(phi_1) / self.width, \
             start[1] + stroke_width * math.sin(phi_1) / self.height
        p2 = start[0] + stroke_width * math.cos(phi_2) / self.width, \
             start[1] + stroke_width * math.sin(phi_2) / self.height
        p3 = end[0] + stroke_width * math.cos(phi_2) / self.width, \
             end[1] + stroke_width * math.sin(phi_2) / self.height
        p4 = end[0] + stroke_width * math.cos(phi_1) / self.width, \
             end[1] + stroke_width * math.sin(phi_1) / self.height

        self.draw_circle(start, r=int(stroke_width / 2), color=color)
        self.draw_circle(end, r=int(stroke_width / 2), color=color)
        self.draw_polygon(p1, p2, p3, p4, color=color)

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