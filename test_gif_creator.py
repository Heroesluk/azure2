from unittest import TestCase

from gif_creator import get_img_links_manually


class Test(TestCase):
    def test_download_album_imgs_manually(self):
        self.assertEqual(get_img_links_manually(["Haru Nemuri_harutosyura"]), {
            'Haru Nemuri_harutosyura': 'https://lastfm.freetls.fastly.net/i/u/300x300/7e1b8d7d7ecd7d713c6de331c7bb866b.jpg'})
