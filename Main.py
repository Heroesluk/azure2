from PIL import Image, ImageColor, UnidentifiedImageError
import colorsys
import os
import random
from collections import Counter
from CreateMosaicIMG import create_maxtrix
from ColorAnalysisAlgorithms import check_if_close_color, check_black_amount, check_white_amount, check_gray_scale

# hsv H:0-1 S:0-1 V: 0-255

im_width, im_height = 900, 900
im = Image.new('RGB', (im_width, im_height))
color = (13, 255, 0)
color_conv = colorsys.rgb_to_hsv(color[0], color[1], color[2])


def create_im_obj(name):
    try:
        return Image.open('AlbumCovers/{}'.format(name))
    except (UnidentifiedImageError, FileNotFoundError) as e:
        print("couldn't open file: {}".format(name), '\n' * 5)
        return False


def analyze_color():
    _albums_color_counter = {}

    for name in os.listdir('AlbumCovers/'):
        try:
            im2 = Image.open('AlbumCovers/{}'.format(name))
        except (UnidentifiedImageError, FileNotFoundError) as e:
            print("couldn't open file: {}".format(name), '\n' * 5)
            continue

        try:
            data2 = list(colorsys.rgb_to_hsv(i[0], i[1], i[2]) for i in im2.getdata())
        except TypeError:
            print("{} could be corrupted".format(name), '\n' * 5)
            continue

        count = 0
        for pixel in data2:
            count += check_black_amount(pixel)

        _albums_color_counter[name] = count
        
    return _albums_color_counter



def print_color_analysis(album_color_count):
    c = Counter(album_color_count)
    for album, count in c.most_common():
        print(album, count)


def generate_mosaic(size, album_color_count):

    images = []
    images_paths = []
    count = 0
    for album, color_count in Counter(album_color_count).most_common():
        temp = Image.open('AlbumCovers/{}'.format(album))
        images_paths.append(album)
        images.append(temp)

        if count >= size*size:
            break

        count += 1

    return images_paths

def main():
    albums_color_counter = analyze_color()

    print_color_analysis(albums_color_counter)
    return generate_mosaic(5, albums_color_counter)






