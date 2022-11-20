from PIL import Image, ImageColor, UnidentifiedImageError
import colorsys
import os
from collections import Counter
from CreateMosaicIMG import create_maxtrix
from ColorAnalysisAlgorithms import check_if_close_color, check_black_amount, check_white_amount, check_gray_scale
from colors import ColorPalette
from database import select_from_id_list
from DownloadDataAndAlbums import get_all_album_img_links, download_album_covers

# hsv H:0-1 S:0-1 V: 0-255

im_width, im_height = 900, 900
im = Image.new('RGB', (im_width, im_height))

clr = ColorPalette()


def color_count_in_img(img_full_path, color, type_of_analysis):
    color_conv = colorsys.rgb_to_hsv(color[0], color[1], color[2])

    try:
        im = Image.open(img_full_path)
        im_hsv = list(colorsys.rgb_to_hsv(i[0], i[1], i[2]) for i in im.getdata())
    except (UnidentifiedImageError, FileNotFoundError, TypeError) as e:
        print("couldn't open file: {}".format(img_full_path), '\n' * 2)
        return False

    count = 0
    for pixel in im_hsv:
        count += check_if_close_color(pixel, color_conv)

    return count


def print_color_analysis(album_color_count):
    c = Counter(album_color_count)
    for album, count in c.most_common():
        print(album, count)


def return_imgs_with_most_color(size, path, color):
    print('huj')
    albums_color_counter = {}

    for name in os.listdir(path):
        albums_color_counter[name] = color_count_in_img('{}/{}'.format(path, name), color, 1)

    images = []
    images_paths = []
    count = 0
    for album, color_count in Counter(albums_color_counter).most_common():
        temp = Image.open('{}/{}'.format(path, album))
        images_paths.append(album)
        images.append(temp)

        if count >= size * size:
            break

        count += 1
    print(images_paths)
    return images_paths


color = clr.PINK

imgs = return_imgs_with_most_color(3, 'AlbumCovers', color)

imgs = select_from_id_list(imgs)

album_dict = {'big' + str(i[0]): i[1] for i in imgs}
download_album_covers(album_dict)

# create_maxtrix(album_dict.keys(), 3)
