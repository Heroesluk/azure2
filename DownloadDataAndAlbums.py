import asyncio
import os

import aiohttp
from itertools import islice
import time

start_time = time.time()


async def fetch(session, name_and_url: tuple, path: str):
    async with session.get(name_and_url[1]) as resp:
        print(name_and_url[1])

        obj = await resp.content.read()
        try:
            with open('{}/{}.jpg'.format(path, name_and_url[0]), 'wb') as f:
                f.write(obj)
        except OSError:
            print(name_and_url[0])

        return 0


#  asynchronously download all images provided list of image links, and name them as index numbers
async def fetch_concurrent(name_url_dict: tuple, path: str):
    count = 0
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = []
        for k, v in name_url_dict:
            tasks.append(loop.create_task(fetch(session, (k, v), path)))

        for result in asyncio.as_completed(tasks):
            await result
            count += 1


def download_album_covers(urls: list, path: str):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # divide urls into 200 sub-dictionaries, which stops asyncio from making too much requests at
    # the same time

    # divided looks like -> [{album_name:album_link},{album_name:album_link}...]
    def chunk(it, size):
        it = iter(it)
        return list(iter(lambda: tuple(islice(it, size)), ()))

    data_divided = chunk(urls, 100)

    for ind, urls_divided in enumerate(data_divided):
        asyncio.run(fetch_concurrent(urls_divided,path))
        print(ind)

        time.sleep(1)


#download_album_covers(read_rows((1, 0, 0, 1, 0, 0)),'AlbumCovers')

print("--- %s seconds ---" % (time.time() - start_time))




