import os

import PIL
import circlify
import requests
import matplotlib
import circlify as circ

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
    def __init__(self, circle: circlify.Circle):
        self.x = 1 - (1 - circle.x) / 2
        self.y = (1 - circle.y) / 2
        self.name = circle.ex['id']
        self.listens = circle.ex['datum']
        self.r = circle.r
        self.path = None

        self.top_x = self.x - self.r
        self.top_y = self.y - self.r

        self.image = None


    def screen_coordinates(self, size):
        return {'x': (self.top_x * size), 'y': (self.top_y * size), 'r': (self.r * size)}

    def get_image(self, path):
        im = Image.open(path)
        im = im.resize((int(self.screen_coordinates(800)['r']),int(self.screen_coordinates(800)['r'])))

        return im

data = [{'id': k, 'datum': float(v[0])} for k, v in artists_data.items()]
circles = circ.circlify(data, show_enclosure=False)





artists_circles = []
for circle in circles:
    temp = CircleToDraw(circle)

    artists_circles.append(temp)

from PIL import Image, ImageDraw

im = Image.new('RGB', (800, 800), (128, 128, 128))
draw = ImageDraw.Draw(im)

import  random
for artists in artists_circles:

    cords = artists.screen_coordinates(800)
    # try:
    #     temp = artists.get_image("Bubbles/" + artists.name + '.png')
    #     im.paste(temp, (cords['x'], cords['y']))
    # except PIL.UnidentifiedImageError:
    #     print(artists.name)


    draw.ellipse((cords['x'], cords['y'], cords['x'] + (cords['r'])
                  , cords['y'] + ( cords['r'])), fill=(random.randrange(1,255), random.randrange(1,255), random.randrange(1,255)))

im.show()
