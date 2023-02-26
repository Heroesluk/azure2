import circlify
import requests



import matplotlib.font_manager as fm
import  matplotlib
#fm._load_fontmanager(try_read_cache=False)

# for f in fm.fontManager.ttflist:
#     print(f)


matplotlib.rcParams['font.family'] = ['IBM Plex Sans JP']



data = requests.get(
    "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=heroesluk&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json&limit=20")


data = data.json()


artists_data = {}

for i in data['topartists']['artist']:
    artists_data[i['name']] = (i['playcount'],i['image'][2]['#text'])
    # print(i['name'], i['playcount'])
    # print(i['image'][2]['#text'])


print(artists_data)




data = [{'id':k,'datum':float(v[0])} for k,v in artists_data.items()]
print(data)
from pprint import pprint as pp
import circlify as circ
#circles = circ.circlify({int(i[0]) for i in artists_data.values()}, show_enclosure=False, datum_field='value')

circles = circ.circlify(data, show_enclosure=False)
print(circles)


circlify.bubbles(circles)



#middle to left top


#midlle to carthesian


class CircleToDraw():
    def __init__(self, circle: circlify.Circle,img_path):
        self.x = 1 - (1 - circle.x) / 2
        self.y = (1 - circle.y) / 2
        self.name = circle.ex['id']
        self.listens = circle.ex['datum']
        self.r = circle.r/2

        self.top_x = self.x-self.r
        self.top_y = self.y-self.r


    def screen_coordinates(self, size):

        return  {'x':self.top_x*size,'y':self.top_y*size, 'r':self.r*size}




artists_circles =  []

for circle in circles:
    temp = CircleToDraw(circle)

    artists_circles.append(temp)




from PIL import Image, ImageDraw

im = Image.new('RGB', (800, 800), (128, 128, 128))
draw = ImageDraw.Draw(im)




for artists in artists_circles:
    cords = artists.screen_coordinates(800)
    draw.ellipse((cords['x'],cords['y'],cords['x']+(2*cords['r'])
                  ,cords['y']+(2*cords['r'])),fill=(255,0,0))



im.show()


