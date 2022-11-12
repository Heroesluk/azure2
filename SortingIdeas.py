
from PIL import  Image, ImageColor, UnidentifiedImageError
import colorsys
import os
import random
from collections import Counter
from Mosaic import create_maxtrix
im_width, im_height = 900, 900


def display_color_band():

    im_width, im_height = 1500, 200
    im = Image.new('RGB', (im_width, im_height))

    colours_length = 100
    colours = []
    for i in range(0, colours_length):
        colours.append(
            (
                random.randrange(0, 359),
                random.randrange(99, 100),
                random.randrange(99, 100)
            )
        )

    print(colours)

    offset = 0
    for color in colours:
        color = ImageColor.getrgb("hsv({}, {}%, {}%)".format(color[0],color[1],color[2]))
        print(color)

        for width in range(im_width // colours_length):
            for height in range(im_height):
                im.putpixel((offset + width, height), color)

        offset += im_width // colours_length

    im.show()

#display_color_band()

def check_if_close(c1,c2):
    hue1,hue2 = c1[0]*359,c2[0]*359
    #if abs(hue1-hue2)<50:
        #print(c2,c1,'value', (abs(hue1-hue2)<50),c1[1],(c1[2]/255))

    return (abs(hue1-hue2)<50)*c2[1]*(c2[2]/255)


#hsv H:0-1 S:0-1 V: 0-255
def draw_hsv():
    for x in range(im_width):
        for y in range(im_height):
            hsv = (x / im_width, 1, int(y * 0.282))
            rgb = tuple(int(i) for i in colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]))

            im.putpixel((x, y), rgb)

    im.show()


im2 = Image.open('AlbumCovers/Karakai.jpg')
data2 = list( colorsys.rgb_to_hsv(i[0],i[1],i[2]) for i in im2.getdata())


im = Image.new('RGB', (im_width, im_height))
color = (0,43,255)
color_conv = colorsys.rgb_to_hsv(color[0],color[1],color[2])
print(color_conv,'0.6272727272727273, 0.7801418439716312, 141')




album_count = {}
for name in os.listdir('AlbumCovers/'):
    try:
        im2 = Image.open('AlbumCovers/{}'.format(name))
    except (UnidentifiedImageError, FileNotFoundError) as e:
        print(name,'zjebalo sie!!!','\n'*5)
        continue


    try:
        data2 = list(colorsys.rgb_to_hsv(i[0],i[1],i[2]) for i in im2.getdata())
    except TypeError:
        print(name,im2.getdata(),'\n'*5)
        continue

    count = 0
    for pixel in data2:
            count += check_if_close(color_conv, pixel)

    print(name, count)
    album_count[name] = count



c = Counter(album_count)
print(c.most_common())
imgs = []
number = 0
for album,count in c.most_common():
    temp = Image.open('AlbumCovers/{}'.format(album))
    imgs.append(temp)

    if number>=9:
        break

    number+=1

create_maxtrix(imgs,3)


##make reference hsv value
#compare in range to something