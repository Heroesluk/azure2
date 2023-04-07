import glob
import os
import unittest
import uuid
from datetime import datetime

import requests

example_album_data = {
    'artist': {
        'mbid': 'f6beac20-5dfe-4d1f-ae02-0b0a740aafd6',
        '#text': 'Tyler, the Creator'
    },
    'mbid': '523f5e88-9988-436d-ab60-6d514c1f0e15',
    'url': 'https://www.last.fm/music/Tyler,+the+Creator/Flower+Boy',
    'name': 'Flower Boy',
    '@attr': {
        'rank': '5'
    },
    'playcount': '345'
}


def clean_up():
    from pathlib import Path

    [f.unlink() for f in Path("GIF").glob("*") if f.is_file()]


from gif_creator import gif_creator, get_img_links_manually, Album, get_record_name
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

    def test_download_album_imgs_manually(self):
        self.assertEqual(get_img_links_manually(["Haru Nemuri_harutosyura"]), {
            'Haru Nemuri_harutosyura': 'https://lastfm.freetls.fastly.net/i/u/300x300/7e1b8d7d7ecd7d713c6de331c7bb866b.jpg'})

    def test_get_record_name(self):
        album = Album(example_album_data)

        self.assertEqual(get_record_name(album), "Tyler, the Creator_Flower Boy")

if __name__ == '__main__':
    unittest.main()
