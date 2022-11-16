import requests as re
import json
import os
from sys import getsizeof
from PIL import Image

import time

start_time = time.time()


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
        data = re.get(
            'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&limit=20&page=&user=heroesluk&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json')
        albums = data.json()
        json.dump(albums, f)


def convert_to_jpg(name, new_name):
    im = Image.open(name)
    bg = Image.new('RGB', im.size)
    bg.paste(im)
    bg.show()

    bg.save(new_name)


class Album():
    def __init__(self, album_js, id):
        self.id = str(id)
        self.name = album_js['name']
        self.artist = album_js['artist']['name']
        self.playcount = int(album_js['playcount'])
        self.rank = int(album_js['@attr']['rank'])

        image_link = album_js['image'][1]['#text']
        extension = image_link[-3:]

        if len(image_link) > 0 and extension in ['jpg', 'png', 'gif']:
            img = re.get(image_link)
            if img.status_code == 200 and getsizeof(img) > 0:
                with open("AlbumCovers/{}.{}".format(self.id, extension), 'wb') as f:
                    f.write(img.content)

                    print(self.id, getsizeof(f))

            else:
                print(img.status_code, getsizeof(img), vars(self))

        else:
            print('no image link', vars(self))


def parse_album_json(name, id_offset):
    links = []
    try:
        with open('Albums/{}'.format(name), 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print('incorrect directory name: {}'.format(name))
        exit()

    for ind, album in enumerate(data['topalbums']['album']):
        temp = album['image'][1]['#text']
        links.append(temp)


    return links



def convert_from_png():
    for file in os.listdir('AlbumCovers/'):
        if file.split('.')[-1] == 'png':

            im = Image.open('AlbumCovers/{}'.format(file))
            rgb_im = im.convert('RGB')

            file_name = '{}.jpg'.format(file[:-4])
            try:
                if file_name not in os.listdir('AlbumCovers/'):
                    rgb_im.save('AlbumCovers/{}'.format(file_name))
                    os.remove('AlbumCovers/{}'.format(file))

            except ValueError or OSError:
                print(file_name, 'sex', file)
                exit()


def _all():
    offset = 0
    for file in os.listdir('Albums/'):
        parse_album_json(file, offset)
        print(file, ' completed')
        offset += 200

urls = parse_album_json('albums1.json',100)


import asyncio
import aiohttp


async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.content.read()
        # Catch HTTP errors/exceptions here

async def fetch_concurrent(urls):
    count = 0
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for u in urls:
            tasks.append(loop.create_task(fetch(session, u)))

        for result in asyncio.as_completed(tasks):
            page = await result
            print(count)
            count+=1
            #Do whatever you want with results

asyncio.run(fetch_concurrent(urls))

print("--- %s seconds ---" % (time.time() - start_time))
