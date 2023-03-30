from unittest import TestCase

from gif_creator import get_img_links_manually, get_record_name
from gif_creator import AlbumFixed


example_album_data =  {
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

class Test(TestCase):
    def test_download_album_imgs_manually(self):
        self.assertEqual(get_img_links_manually(["Haru Nemuri_harutosyura"]), {
            'Haru Nemuri_harutosyura': 'https://lastfm.freetls.fastly.net/i/u/300x300/7e1b8d7d7ecd7d713c6de331c7bb866b.jpg'})


    def test_get_record_name(self):
        album = AlbumFixed(example_album_data)

        self.assertEqual(get_record_name(album),"Tyler, the Creator_Flower Boy")
