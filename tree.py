import requests as re
import json

from PIL import Image

def get_albums():
    for i in range(10):
        with open('Albums/albums{}.json'.format(i), 'w') as f:
            data = re.get(
                'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&limit=200&page={}&user=heroesluk&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json'.format(
                    i))
            albums = data.json()
            json.dump(albums, f)

    print(data.content)


def test_album():
    with open('Albums/albums_test.json', 'w') as f:
        data = re.get('http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&limit=20&page=&user=heroesluk&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json')
        albums = data.json()
        json.dump(albums, f)



def convert_to_jpg(name, new_name):
    im = Image.open(name)
    bg = Image.new('RGB', im.size)
    bg.paste(im)
    bg.show()

    bg.save(new_name)



def download_album_covers():
    errors = []

    with open('Albums/albums3.json','r') as f:
       data = json.load(f)
    for album in data['topalbums']['album']:

        s,m,l = album['image'][0]['#text'],album['image'][1]['#text'],album['image'][2]['#text']
        if len(m)>0:
            img = re.get(album['image'][1]['#text'])
        elif len(s)>0:
            img = re.get(album['image'][2]['#text'])
        elif len(l)>0:
            img = re.get(album['image'][3]['#text'])
        else:
            print('no image for', album)

            continue

        img_type = album['image'][1]['#text'].split('.')[-1]

        if img.status_code == 200:
            try:
                with open('AlbumCovers/{}.{}'.format(album['name'], img_type), 'wb') as f:
                    f.write(img.content)
            except OSError as e:
                print(album['image'], e)

        else:
            print(album['artist']['name'], album['name'], album['playcount'], album['image'][1]['#text'])
            print(img.status_code)


import os

def convert_from_png():
    for file in os.listdir('AlbumCovers/'):
        if file.split('.')[-1] == 'png':

            im = Image.open('AlbumCovers/{}'.format(file))
            rgb_im = im.convert('RGB')

            file_name = '{}.jpg'.format(file.split('.')[0])

            try:
                if file_name not in os.listdir('AlbumCovers/'):
                    rgb_im.save('AlbumCovers/{}'.format(file_name))
            except ValueError or OSError:
                print(file_name,'sex',file)
                exit()

            os.remove('AlbumCovers/{}'.format(file))


#convert_from_png()

os.chdir('AlbumCovers/')
for file in os.listdir():
    if os.stat(file.rstrip()).st_size == 0:
        print("removing: ",file)
        os.remove(file)
