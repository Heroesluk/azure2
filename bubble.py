import os

import PIL
import circlify
import requests
import matplotlib
import circlify as circ
from PIL import Image, ImageDraw
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

data = [{'id': k, 'datum': float(v[0])} for k, v in artists_data.items()]
circles = circ.circlify(data, show_enclosure=False)


import circlify
import matplotlib.pyplot as plt

# Create just a figure and only one subplot
fig, ax = plt.subplots(figsize=(10,10))

# Remove axes
ax.axis('off')

# Find axis boundaries
lim = max(
    max(
        abs(circle.x) + circle.r,
        abs(circle.y) + circle.r,
    )
    for circle in circles
)


plt.xlim(-lim, lim)
plt.ylim(-lim, lim)





im = Image.new('RGB', (1000, 1000), (128, 128, 128))
draw = ImageDraw.Draw(im)

for circle in circles:
    x, y, r = circle
    print(circle)
    ax.add_patch(plt.Circle((x, y), r, alpha=0.2, linewidth=2, fill=False))
#
#     draw.ellipse(((1+x)/2,(1+y)/2, ((1+x)/2)+r,((1+y)/2)+r),
#                  fill=(random.randrange(1, 255), random.randrange(1, 255), random.randrange(1, 255)))

# plt.show()



artists_circles = []
# for circle in circles:
#     temp = CircleToDraw(circle)
#     artists_circles.append(temp)
# for artists in artists_circles:
#
#     cords = artists.screen_coordinates(800)
#     # try:
#     #     temp = artists.get_image("Bubbles/" + artists.name + '.png')
#     #     im.paste(temp, (cords['x'], cords['y']))
#     # except PIL.UnidentifiedImageError:
#     #     print(artists.name)
#
#
#     draw.ellipse((cords['x'], cords['y'], cords['x'] + (cords['r'])
#                   , cords['y'] + (cords['r'])), fill=(random.randrange(1,255), random.randrange(1,255), random.randrange(1,255)))
#
# im.show()


cn: Canvas = Canvas(size=(800,800))

for circle in circles:
    x,y,r = circle.x, circle.y, circle.r
    l,r,u,low = cn.give_circle_coords((x,y),r*400,(random.randrange(1,255), random.randrange(1,255), random.randrange(1,255)))
    draw.ellipse((l, r, u, low), fill=(123,0,0), outline=None)

    name = circle.ex['id']
    try:
        img = Image.open("Bubbles/" + name + ".png")
        img = img.resize((int(u-l),int(low-r)))
        im.paste(img, (int(l),int(r)))
    except (FileNotFoundError, PIL.UnidentifiedImageError):
        print(name)


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

im.show()


# cn.img.show()
