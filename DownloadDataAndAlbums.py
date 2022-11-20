import requests as re
import json
import os
from sys import getsizeof
from PIL import Image
import asyncio
import aiohttp
import time
from itertools import islice
from colors import *
from database import *

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


def get_all_album_img_links(size, search_key=False):
    links = []
    names = []
    try:
        with open('albums.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print('incorrect directory name: {}')
        exit()

    for ind, album in enumerate(data):
        temp = album["image"][size]['#text']  # size: 0 - small, 1- medium, 2 large 3 extra-large,
        name = album['name'] + '.jpg'

        # 1 is to medium, and 2 big - > #text for some reason is where the image link is

        if len(temp) > 0 and len(name) > 0:  # check if link actually exist, if no then ignore album
            links.append(temp)
            names.append(name)
        else:
            print('error', temp, name)

    return {i[0]: i[1] for i in zip(names, links)}


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


async def fetch(session, name_and_url: tuple):
    async with session.get(name_and_url[1]) as resp:
        obj = await resp.content.read()
        try:
            with open('AlbumCovers/{}.jpg'.format(name_and_url[0]), 'wb') as f:
                f.write(obj)
        except OSError:
            print(name_and_url[0])


        return 0


def divide(_urls):
    def chunks(data, SIZE=10000):
        it = iter(data)
        for i in range(0, len(data), SIZE):
            yield {k: data[k] for k in islice(it, SIZE)}

    divided = []

    for item in chunks(_urls, 200):
        divided.append(item)

    return divided


#  asynchronously download all images provided list of image links, and name them as index numbers
async def fetch_concurrent(name_url_dict: dict):
    count = 0
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for k, v in name_url_dict.items():
            tasks.append(loop.create_task(fetch(session, (k, v))))

        for result in asyncio.as_completed(tasks):
            page = await result
            count += 1


def download_album_covers(name_url_dict: dict):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    divided = divide(
        name_url_dict)  # divide urls into 200 sub-dictionaries, which stops asyncio from making too much requests at
    # the same time

    # divided looks like -> [{album_name:album_link},{album_name:album_link}...]
    for ind, urls_divided in enumerate(divided):
        asyncio.run(fetch_concurrent(urls_divided))
        print(ind)

        time.sleep(3)


#data = parse_json('albums.json')
data_dict = readSqliteTable()
print(data_dict)
#download_album_covers(data_dict)



print("--- %s seconds ---" % (time.time() - start_time))
# TODO: save images based on something other then index, since async make it impossible to guess based on name what album it is
# i should probably serialize this json
