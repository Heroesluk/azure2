import os
from itertools import product
from PIL import Image
import math

def color_palette_range():
    col_number = 2
    colors = product((0, 124, 248), repeat=3)
    col2 = [tuple(reversed(i)) for i in colors] + list(colors)

    return col2

def simplify_color(_data):
    for i in _data:
        for d, v in enumerate(i):
            if v >= 250:
                i[d] = 249

    divisor =  249//2
    print(divisor)

    for index, _rgb in enumerate(_data):
        _data[index] = ((_rgb[0]//divisor)*divisor,(_rgb[1]//divisor)*divisor,(_rgb[2]//divisor)*divisor)

    return _data



def count_colors(_data,col_palette):
    color_count = {i: 0 for i in set(col_palette)}
    for index, _rgb in enumerate(_data):
        color_count[_rgb] += 1
    return color_count

def print_out_colors(_color_count):
    from collections import Counter

    c = Counter(_color_count)
    print(c.most_common())



#porownujemy kolory na albumie, do referencyjnego koloru, oraz zblizonych mu w deltcie(np50) kolorach

im = Image.open('AlbumCovers/Atom Heart Mother.jpg')
data = list(list(i) for i in im.getdata())

im.show()
count = count_colors(data,color_palette_range())
print_out_colors(count)
#values: 0, 248, 124

reference = (128, 128, 0)


def compare(album_color_count, reference_color):
    return album_color_count[reference_color]


def main():
    album_counts = {}


    for name in os.listdir('AlbumCovers/'):
        im = Image.open('AlbumCovers/{}'.format(name))
        data = list(list(i) for i in im.getdata())
        data = simplify_color(data)
        album_counts[name] = count_colors(data)

    for k, v in album_counts.items():
        try:
            print(k, v[reference], v)
        except KeyError:
            pass



