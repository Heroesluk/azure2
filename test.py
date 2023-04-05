import glob
import os
import unittest
from datetime import datetime


def clean_up():
    from pathlib import Path

    [f.unlink() for f in Path("GIF").glob("*") if f.is_file()]


from gif_creator import gif_creator


class MyTestCase(unittest.TestCase):
    def test_something(self):
        clean_up()

        gif_creator(datetime(2022, 6, 1), "month", 4), datetime(2022, 12, 1)
        self.assertEqual(len(os.listdir("GIF")), 96)  # add assertion here


if __name__ == '__main__':
    unittest.main()
