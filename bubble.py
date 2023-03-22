import os

import PIL
import circlify
import requests
import matplotlib
import circlify as circ
from PIL import Image, ImageDraw, ImageChops, ImageOps
import  random

from pathvalidate import ValidationError, validate_filename, sanitize_filename



from stolen import *


"""Since lastfm refuse to give image links for gettopartists
it has to be done manually by fetching albums, and then match album covers with corresponding artists
since the whole purpose of this script it to display most listened artists,
 we can assume that artist from top50 will have at least 1 album within top500 albums
 
 
 Returns dict in format of {artist_name: (play_counts, img_link)}
 """
def get_top_listened_artists_with_img_links(user: str, limit: int):
    data = requests.get(
        "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={}&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json".format(user))
    top_artists = data.json()['topartists']

    top_albums = requests.get(
        'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={}&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json&limit={}'.format(user,limit)).json()['topalbums']

    artists_data = {}
    keys = {}

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



def get_top_listened_albums_with_img_links(user: str, limit:int):
    print('http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={}&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json&limit={}'.format(user,limit))
    images_data = requests.get(
        'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={}&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json&limit={}'.format(user,limit)).json()

    artists_data = {}
    keyz = {}


    for i in images_data['topalbums']['album']:
        if i['artist']['name'] not in keyz.keys():
            artists_data[sanitize_filename(i['name'])] = (i['playcount'],i['image'][2]['#text'])




    return artists_data







def download_image(_data):
    saved = [i for i in os.listdir('Bubbles')]

    for artist_name, (play_count, link) in _data.items():
        if len(link) > 0:
            if artist_name not in saved:
                try:
                    img = requests.get(link).content

                    with open('Bubbles/{}.png'.format(artist_name), 'wb') as f:
                        f.write(img)

                except KeyError:
                    print("No image for: {}".format(artist_name))


artist_data = get_top_listened_albums_with_img_links("IDieScreaming",30)

download_image(artist_data)





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



def main():

    data = [{'id': k, 'datum': pow(float(v[0]),1.5)} for k, v in artist_data.items()]
    circles = circ.circlify(data, show_enclosure=False)

    im = Image.new('RGB', (800, 800), (128, 128, 128))
    draw = ImageDraw.Draw(im)

    artists_circles = []

    cn: Canvas = Canvas(size=(800, 800))

    for circle in circles:
        x, y, r = circle.x, circle.y, circle.r
        l, r, u, low = cn.give_circle_coords((x, y), r * 400, (
        random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255)))

        name = circle.ex['id']
        try:
            img = Image.open("Bubbles/" + name + ".png")

            img = image_to_circle(img)
            img = img.resize((int(u - l), int(low - r)))

            im.paste(img, (int(l), int(r)),img)
        except (FileNotFoundError, PIL.UnidentifiedImageError):
            print(name)

    im.show()


main()
