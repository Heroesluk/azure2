import os
from concurrent.futures import as_completed

from PIL import Image, ImageDraw, UnidentifiedImageError
import requests
import circlify as circ
import random
from requests_futures.sessions import FuturesSession

from pathvalidate import sanitize_filename


class ConvertToCarthesian:
    """
    Represents an image on which to draw
    The center of the image is considered (0, 0). The corners are (-1, 1), (1, 1), (1, -1) and (-1, -1)
    """

    # TODO: Use this Canvas in Pointillizer

    def __init__(self, size=(800, 800)):
        self.width, self.height = size

    def give_circle_coords(self, pos, r: int, color):
        x, y = pos
        left = self._rel_x_to_abs_x(x) - r
        right = self._rel_x_to_abs_x(x) + r
        upper = self._rel_y_to_abs_y(y) - r
        lower = self._rel_y_to_abs_y(y) + r
        return left, upper, right, lower

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


"""Since lastfm refuse to give image links for gettopartists
it has to be done manually by fetching albums, and then match album covers with corresponding artists
since the whole purpose of this script it to display most listened artists,
 we can assume that artist from top50 will have at least 1 album within top500 albums


 Returns dict in format of {artist_name: (play_counts, img_link)}
 """


def get_top_listened_artists_with_img_links(user: str, limit: int):
    data = requests.get(
        "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={}&api_key=d6e02ae58fcf6daaea788ce99c879f9c&limit={}&format=json".format(
            user, limit))
    top_artists = data.json()['topartists']

    top_albums = requests.get(
        'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={}&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json&limit={}'.format(
            user, limit)).json()['topalbums']

    artists_data = {}
    keys = {}
    ##TODO: change image size depending on the size
    for i in top_albums['album']:
        if i['artist']['name'] not in keys.keys():
            # {artist_name:image_link} where 2 corresponds to size of image
            keys[i['artist']['name']] = i['image'][2]['#text']

    for i in top_artists['artist']:
        try:
            artists_data[sanitize_filename(i['name'])] = (float(i['playcount']), keys[i['name']])
        except KeyError:
            print("No image for {}".format(i['name']))

    return artists_data


##size 100 is most optimal upper limit, after it circlify slows downs significantly
def get_top_listened_albums_with_img_links(user: str, limit: int):
    print(
        'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={}&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json&limit={}'.format(
            user, limit))
    images_data = requests.get(
        'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={}&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json&limit={}'.format(
            user, limit)).json()

    artists_data = {}
    keyz = {}

    for i in images_data['topalbums']['album']:
        if i['artist']['name'] not in keyz.keys():
            artists_data[sanitize_filename(i['name'])] = (i['playcount'], i['image'][2]['#text'])

    return artists_data


def async_down(_data):
    session = FuturesSession(max_workers=20)
    if not os.path.exists("Bubbles"):
        os.makedirs("Bubbles")
    futures = []

    for artist_name, (play_count, link) in _data.items():
        if len(link) > 0:
            future = session.get(link)
            future.name = artist_name
            futures.append(future)

    for future in as_completed(futures):
        resp = future.result()

        with open('Bubbles/{}.png'.format(future.name), 'wb') as f:
            f.write(resp.content)


def image_to_circle(img: Image):
    ##TODO: maybe some optimalization? need to test if predefined
    ##mask size wont break anything
    bigsize = (img.size[0] * 3, img.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(img.size, Image.ANTIALIAS)
    img.putalpha(mask)

    return img


def main(bubble_type: str, size: int, nickname: str):
    if bubble_type == 'album':
        artist_data = get_top_listened_albums_with_img_links(nickname, size)
    elif bubble_type == 'artist':
        artist_data = get_top_listened_artists_with_img_links(nickname, size)
    else:
        raise AttributeError("Incorrect bubble type")

    if size > 100 or size < 10:
        raise AttributeError("Incorrect size")
    elif len(nickname) == 0:
        raise AttributeError("No nickname specified")

    async_down(artist_data)

    data = [{'id': k, 'datum': pow(float(v[0]), 1.5)} for k, v in artist_data.items()]
    circles = circ.circlify(data, show_enclosure=False)

    im = Image.new('RGB', (800, 800), (128, 128, 128))
    cn: ConvertToCarthesian = ConvertToCarthesian(size=(800, 800))

    for circle in circles:
        x, y, r = circle.x, circle.y, circle.r
        l, r, u, low = cn.give_circle_coords((x, y), r * 400, (
            random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255)))

        name = circle.ex['id']
        try:
            img = Image.open("Bubbles/" + name + ".png")

            img = image_to_circle(img)
            img = img.resize((int(u - l), int(low - r)))

            im.paste(img, (int(l), int(r)), img)
        except (FileNotFoundError, UnidentifiedImageError, ValueError):
            print(name)

    im.save("static/bubble.png")
