import requests as re
import json
import os
from sys import getsizeof
from PIL import Image
import asyncio
import aiohttp
import time

start_time = time.time()


# heroesluk

# number of albums is multiplied by 1000,
# since limit above 500 remove image links from response(probably bc of request size?)
# i multiply n_o_a by 2 to achieve desired number
def create_albums_json(user, number_of_albums):
    data_to_append = []
    for i in range(1, (number_of_albums * 2) + 1):
        data = re.get(
            'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&limit=500&page={}&user={}&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json'.format(
                i, user))

        albums = data.json()
        data_to_append.append(albums)

    head = data_to_append[0]['topalbums']['album']
    for i in data_to_append[1:]:
        head += i['topalbums']['album']

    with open('albums.json', 'w') as f:
        json.dump(head, f)


def get_all_small_album_img_links():
    links = []
    try:
        with open('albums.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print('incorrect directory name: {}')
        exit()

    for ind, album in enumerate(data):
        temp = album["image"][0]['#text']  # index 0 refers to image size in json,
        # 1 is to medium, and 2 big - > #text for some reason is where the image link is

        if len(temp) > 0:  # check if link actually exist, if no then ignore album
            links.append(temp)

    return links


from itertools import islice


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.content.read()

#  asynchronously download all images provided list of image links, and name them as index numbers
async def fetch_concurrent(urls):
    count = 0
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for u in urls:
            tasks.append(loop.create_task(fetch(session, u)))

        for result in asyncio.as_completed(tasks):

            page = await result

            with open('AlbumCovers/{}.jpg'.format(count), 'wb') as f:
                f.write(page)

            count+=1


def _all():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    urls = get_all_small_album_img_links()
    divided = chunk(urls, 200)
    for ind, urls_divided in enumerate(divided):
        asyncio.run(fetch_concurrent(urls_divided))
        time.sleep(3)
        print(ind)

_all()

print("--- %s seconds ---" % (time.time() - start_time))
#TODO: save images based on something other then index, since async make it impossible to guess based on name what album it is
#i should probably serialize this json
