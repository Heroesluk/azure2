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


        if len(temp)>0:
            links.append(temp)


    return links


import asyncio
import aiohttp


async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.content.read()
        # Catch HTTP errors/exceptions here

async def fetch_concurrent(urls,offset):
    count = offset
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for u in urls:
            tasks.append(loop.create_task(fetch(session, u)))

        for result in asyncio.as_completed(tasks):
            page = await result

            with open('AlbumCovers/{}.jpg'.format(count),'wb') as f:
                f.write(page)


            count+=1
            #Do whatever you want with results


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def _all():
    offset = 0
    for file in os.listdir('Albums/'):
        urls = parse_album_json(file, offset)
        asyncio.run(fetch_concurrent(urls,offset))


        print(file, ' completed')
        offset += 200

_all()


print("--- %s seconds ---" % (time.time() - start_time))

