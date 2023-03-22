import os

import PIL
import circlify
import requests
import matplotlib
import circlify as circ
from PIL import Image, ImageDraw, ImageChops, ImageOps
import  random



from stolen import *


"""Since lastfm refuse to give image links for gettopartists
it has to be done manually by fetching albums, and then match album covers with corresponding artists
since the whole purpose of this script it to display most listened artists,
 we can assume that artist from top50 will have at least 1 album within top500 albums"""
def get_top_listened_artists_with_img_links(user: str):
    data = requests.get(
        "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={}&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json".format(user))
    data = data.json()

    images_data = requests.get(
        'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={}&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json&limit=500'.format(user)).json()

    artists_data = {}
    keyz = {}

    for i in images_data['topalbums']['album']:
        if i['artist']['name'] not in keyz.keys():
            keyz[i['artist']['name']] = i['image'][2]['#text']

    for i in data['topartists']['artist']:
        try:
            artists_data[i['name']] = (i['playcount'], keyz[i['name']])
        except KeyError:
            print("No image for {}".format(i['name']))


    return artists_data


def get_top_listened_albums_with_img_links(user: str):

    images_data = requests.get(
        'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={}&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json&limit=500'.format(user)).json()

    artists_data = {}
    keyz = {}

    print(images_data)
    exit()

    for i in images_data['topalbums']['album']:
        if i['artist']['name'] not in keyz.keys():
            keyz[i['artist']['name']] = i['image'][2]['#text']




    return artists_data



artist_data = get_top_listened_artists_with_img_links("IDieScreaming")



def download_image(_data):
    for k, v in _data.items():

        if len(v[1]) > 0:
            try:
                img = requests.get(v[1]).content

                with open('Bubbles/{}.png'.format(k), 'wb') as f:
                    f.write(img)

            except KeyError:
                print("No image for: {}".format(k))


# download_image(artist_data)





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
