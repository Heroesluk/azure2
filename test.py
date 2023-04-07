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

    def test_something(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

        self.assertEqual(main("album", 50,"lkdjflkshdjfkhdskjfh","TestOutputs/1"),None)
        self.assertEqual(main("album", 50, "heroesluk", "TestOutputs/3"), "TestOutputs/3")



# if __name__ == '__main__':
#     unittest.main()





