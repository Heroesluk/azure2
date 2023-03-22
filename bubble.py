import os

import PIL
import circlify
import requests
import matplotlib
import circlify as circ
from PIL import Image, ImageDraw, ImageChops, ImageOps
import  random


from stolen import *


data = requests.get(
    "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=heroesluk&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json")
data = data.json()

images_data = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user=heroesluk&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json&limit=500').json()



artists_data = {}
keyz = {}

for i in images_data['topalbums']['album']:
    if i['artist']['name'] not in keyz.keys():
        keyz[i['artist']['name']] =  i['image'][2]['#text']



print(data)
for i in data['topartists']['artist']:
    try:
        artists_data[i['name']] = (i['playcount'], keyz[i['name']])
    except KeyError:
        print("No image for {}".format(i['name']))



def download_image(_data):
    for k,v in _data.items():

        if len(v[1])>0:
            try:
                img = requests.get(v[1]).content

                with open('Bubble'
                          ''
                          's/{}.png'.format(k), 'wb') as f:
                    f.write(img)

            except KeyError:
                print("No image for: {}".format(k))


#download_image(artists_data)




class CircleToDraw():
    def __init__(self, circle: circlify.Circle,left,upper,right,lower):
        self.left = left
        self.right = right
        self.upper = upper
        self.lower = lower
        self.name = circle.ex['id']
        self.listens = circle.ex['datum']
        self.r = circle.r
        self.path = None



        self.image = None


    def screen_coordinates(self, size):
        return {'x': (self.top_x * size), 'y': (self.top_y * size), 'r': (self.r * size)}

    def get_image(self, path):
        im = Image.open(path)
        im = im.resize((int(self.screen_coordinates(800)['r']),int(self.screen_coordinates(800)['r'])))

        return im


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
    data = [{'id': k, 'datum': float(v[0])} for k, v in artists_data.items()]
    circles = circ.circlify(data, show_enclosure=False)

    im = Image.new('RGB', (1000, 1000), (128, 128, 128))
    draw = ImageDraw.Draw(im)

    artists_circles = []

    cn: Canvas = Canvas(size=(800, 800))

    for circle in circles:
        x, y, r = circle.x, circle.y, circle.r
        l, r, u, low = cn.give_circle_coords((x, y), r * 400, (
        random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255)))
        # draw.ellipse((l, r, u, low), fill=(123, 0, 0), outline=None)

        name = circle.ex['id']
        try:
            img = Image.open("Bubbles/" + name + ".png")

            img = image_to_circle(img)
            img = img.resize((int(u - l), int(low - r)))

            im.paste(img, (int(l), int(r)),img)
        except (FileNotFoundError, PIL.UnidentifiedImageError):
            print(name)

    im.show()

    # artists_circles.append(CircleToDraw(circle, l,r,u,low))
    # cn.draw_circle((x,y),r*400,(random.randrange(1,255), random.randrange(1,255), random.randrange(1,255)))

#
# for artists in artists_circles:
#
#     cords = artists.screen_coordinates(800)
#     try:
#         temp = artists.get_image("Bubbles/" + artists.name + '.png')
#         im.paste(temp, (artists.left,artists.upper))
#     except PIL.UnidentifiedImageError:
#         print(artists.name)

    #
    # draw.ellipse((cords['x'], cords['y'], cords['x'] + (cords['r'])
    #               , cords['y'] + (cords['r'])), fill=(random.randrange(1,255), random.randrange(1,255), random.randrange(1,255)))



main()
