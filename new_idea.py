import os
from PIL import Image
from math import  pow, sqrt
from collections import Counter


# https://www.baeldung.com/cs/compute-similarity-of-colours
def distance(c1,c2):
    return sqrt(pow((c1[0]-c2[0]),2)*0.3) + (pow((c1[1]-c2[1]),2)*0.59) + (pow((c1[2]-c2[2]),2)*0.11)

reference = (255,165,0)

color_count = {reference:0}
similar_count = {}

def main():
    for name in os.listdir('AlbumCovers/'):
        im = Image.open('AlbumCovers/{}'.format(name))
        im.convert('RGB')
        data = list(i for i in im.getdata())

        similar_count[name] = 0

        for i in data:
            if distance(i, reference) < 1000:
                similar_count[name] += 1

    print(similar_count)

    for i in (Counter(similar_count).most_common()):
        if 'Third' in i[0]:
            print(i)

main()