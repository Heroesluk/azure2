import os
from PIL import Image, ImageColor
from math import pow, sqrt
from collections import Counter
import colorsys
import random


def draw_hsv():
    im = Image.new('RGB', (900, 900))

    for x in range(900):
        for y in range(900):
            hsv = (x / 900, 1, int(y * 0.282))
            rgb = tuple(int(i) for i in colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]))

            im.putpixel((x, y), rgb)

    im.show()


def display_color_band():
    im_width, im_height = 1500, 200
    im = Image.new('RGB', (im_width, im_height))

    colours_length = 100
    colours = []
    for i in range(0, colours_length):
        colours.append(
            (
                random.randrange(0, 359),
                random.randrange(99, 100),
                random.randrange(99, 100)
            )
        )

    print(colours)

    offset = 0
    for color in colours:
        color = ImageColor.getrgb("hsv({}, {}%, {}%)".format(color[0], color[1], color[2]))
        print(color)

        for width in range(im_width // colours_length):
            for height in range(im_height):
                im.putpixel((offset + width, height), color)

        offset += im_width // colours_length

    im.show()


# https://www.baeldung.com/cs/compute-similarity-of-colours
def distance(c1, c2):
    return sqrt(pow((c1[0] - c2[0]), 2) * 0.3) + (pow((c1[1] - c2[1]), 2) * 0.59) + (pow((c1[2] - c2[2]), 2) * 0.11)


def main():
    reference = (255, 165, 0)

    color_count = {reference: 0}
    similar_count = {}

    for name in os.listdir('AlbumCovers/'):
        im = Image.open('AlbumCovers/{}'.format(name))
        im.convert('RGB')
        data = list(i for i in im.getdata())

        similar_count[name] = 0

        for i in data:
            if distance(i, reference) < 1000:
                similar_count[name] += 1

    print(similar_count)

    for i in (Counter(similar_count).most_common()):
        if 'Third' in i[0]:
            print(i)


draw_hsv()


def test_album():
    with open('Albums/albums_test.json', 'w') as f:
        data = re.get(
            'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&limit=20&page=&user=heroesluk&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json')
        albums = data.json()
        json.dump(albums, f)


def convert_to_jpg(name, new_name):
    im = Image.open(name)
    bg = Image.new('RGB', im.size)
    bg.paste(im)
    bg.show()

    bg.save(new_name)


class Album():
    def __init__(self, album_js, id):
        self.id = str(id)
        self.name = album_js['name']
        self.artist = album_js['artist']['name']
        self.playcount = int(album_js['playcount'])
        self.rank = int(album_js['@attr']['rank'])

        image_link = album_js['image'][1]['#text']
        extension = image_link[-3:]

        if len(image_link) > 0 and extension in ['jpg', 'png', 'gif']:
            img = re.get(image_link)
            if img.status_code == 200 and getsizeof(img) > 0:
                with open("AlbumCovers/{}.{}".format(self.id, extension), 'wb') as f:
                    f.write(img.content)

                    print(self.id, getsizeof(f))

            else:
                print(img.status_code, getsizeof(img), vars(self))

        else:
            print('no image link', vars(self))


def convert_from_png():
    for file in os.listdir('AlbumCovers/'):
        if file.split('.')[-1] == 'png':

            im = Image.open('AlbumCovers/{}'.format(file))
            rgb_im = im.convert('RGB')

            file_name = '{}.jpg'.format(file[:-4])
            try:
                if file_name not in os.listdir('AlbumCovers/'):
                    rgb_im.save('AlbumCovers/{}'.format(file_name))
                    os.remove('AlbumCovers/{}'.format(file))

            except ValueError or OSError:
                print(file_name, 'sex', file)
                exit()
