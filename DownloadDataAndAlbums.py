import asyncio
import aiohttp
from itertools import islice
from database import *

start_time = time.time()


# number of albums is multiplied by 1000,
# since limit above 500 remove image links from response(probably bc of request size?)
# i multiply n_o_a by 2 to achieve desired number


async def fetch(session, name_and_url: tuple):
    async with session.get(name_and_url[1]) as resp:
        obj = await resp.content.read()
        try:
            with open('AlbumCovers/{}.jpg'.format(name_and_url[0]), 'wb') as f:
                f.write(obj)
        except OSError:
            print(name_and_url[0])

        return 0


#  asynchronously download all images provided list of image links, and name them as index numbers
async def fetch_concurrent(name_url_dict: tuple):
    count = 0
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for k, v in name_url_dict:
            tasks.append(loop.create_task(fetch(session, (k, v))))

        for result in asyncio.as_completed(tasks):
            await result
            count += 1


def download_album_covers(urls):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # divide urls into 200 sub-dictionaries, which stops asyncio from making too much requests at
    # the same time

    # divided looks like -> [{album_name:album_link},{album_name:album_link}...]
    data_divided = chunk(urls, 200)

    for ind, urls_divided in enumerate(data_divided):
        asyncio.run(fetch_concurrent(urls_divided))
        print(ind)

        time.sleep(3)


def chunk(it, size):
    it = iter(it)
    return list(iter(lambda: tuple(islice(it, size)), ()))


# data = parse_json('albums.json')
data = read_rows()[:400]
download_album_covers(data)


print("--- %s seconds ---" % (time.time() - start_time))
# TODO: save images based on something other then index,
#  since async make it impossible to guess based on name what album it is
# i should probably serialize this json
