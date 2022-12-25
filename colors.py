from typing import Tuple


class ColorPalette():
    def __init__(self):
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 128, 0)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 128, 255)
        self.VIOLET = (127, 0, 255)
        self.PINK = (255, 0, 127)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

    def access_by_name(self, color: str) -> Tuple[int, int, int]:
        try:
            return getattr(self, color.lower())
        except AttributeError:
            print('color doesnt exist in the palette, returning white color ')
            return self.WHITE
