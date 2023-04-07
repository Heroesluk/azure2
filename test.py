import glob
import os
import unittest
import uuid
from datetime import datetime

import requests


def clean_up():
    from pathlib import Path

    [f.unlink() for f in Path("GIF").glob("*") if f.is_file()]


from gif_creator import gif_creator
from bubble import main

import warnings


class MyTestCase(unittest.TestCase):

    def test_bubbles(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

        self.assertEqual(main("album", 50, "lkdjflkshdjfkhdskjfh", "TestOutputs/1"), None)
        self.assertEqual(main("album", 50, "heroesluk", "TestOutputs/3"), "TestOutputs/3")

    def test_gif(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

        self.assertEqual(gif_creator(datetime.strptime("2022-01-01", "%Y-%m-%d"), "6month", 4,
                                     "2c77d688-eeb1-40d1-a3ae-ccf30e7d6aee",
                                     "nemesis"), None)

        self.assertTrue(gif_creator(datetime.strptime("2022-01-01", "%Y-%m-%d"), "6month", 4,
                          "2c77d688-eeb1-40d1-a3ae-ccf30e7d6aee",
                          "heroesluk"))

        self.assertIsNone(gif_creator(datetime.strptime("2022-01-01", "%Y-%m-%d"), "6month", 4,
                          "2c77d688-eeb1-40d1-a3ae-ccf30e7d6aee",
                          "shdkjahkjshjd"))

# if __name__ == '__main__':
#     unittest.main()
