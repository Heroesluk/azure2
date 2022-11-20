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
color = (0, 123, 255)
color_conv = colorsys.rgb_to_hsv(color[0], color[1], color[2])


def analyze_color(path):
    _albums_color_counter = {}

    for name in os.listdir(path):
        try:
            im2 = Image.open('{}/{}'.format(path,name))
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
            count += check_if_close_color(pixel,color_conv)

        _albums_color_counter[name] = count
        
    return _albums_color_counter



def print_color_analysis(album_color_count):
    c = Counter(album_color_count)
    for album, count in c.most_common():
        print(album, count)


def generate_mosaic(size,path):
    album_color_count = analyze_color('AlbumCovers')


    images = []
    images_paths = []
    count = 0
    for album, color_count in Counter(album_color_count).most_common():
        temp = Image.open('{}/{}'.format(path,album))
        images_paths.append(album)
        images.append(temp)

        if count >= size*size:
            break

        count += 1
    print(images_paths)
    return images_paths


imgs = generate_mosaic(3,'AlbumCovers')

create_maxtrix(imgs,3)









