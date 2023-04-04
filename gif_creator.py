import cProfile
from concurrent.futures import as_completed
from pathvalidate import sanitize_filename

import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Tuple, Dict
import os
import imageio
from PIL import Image
from requests_futures.sessions import FuturesSession
import io

files = []


def clean_up():
    from pathlib import Path

    [f.unlink() for f in Path("GIF").glob("*") if f.is_file()]


def convert_last_album_cover_link_to_id(link: str):
    return (link.split("/")[-1]).split('.jpg')[0]


# since lastfm weeklychart
# http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user=Heroesluk&limit=1000&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json
def top_albums_dict():
    data = requests.get(
        "http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&use"
        "r=Heroesluk&limit=1000&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json").json()

    return {i['url']: i for i in data['topalbums']['album']}


def top_albums_images():
    data = requests.get(
        "http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&use"
        "r=Heroesluk&limit=500&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json").json()

    return {sanitize_filename(i['artist']['name'] + "_" + i['name']): i['image'][3]['#text'] for i in
            data['topalbums']['album']}


print(top_albums_images())


class AlbumFixed():
    def __init__(self, data):
        self.artist = data['artist']['#text']
        self.album_name = data['name']
        self.url = data['url']

        self.rank = int(data["@attr"]['rank'])
        self.play_count = int(data['playcount'])

        self.image_path = get_record_name(self)

        self.image = None


# in a format of {
#         'artist': {
#           'mbid': 'f6beac20-5dfe-4d1f-ae02-0b0a740aafd6',
#           '#text': 'Tyler, the Creator'
#         },
#         'mbid': '523f5e88-9988-436d-ab60-6d514c1f0e15',
#         'url': 'https://www.last.fm/music/Tyler,+the+Creator/Flower+Boy',
#         'name': 'Flower Boy',
#         '@attr': {
#           'rank': '5'
#         },
#         'playcount': '345'
#       }
# returns list of most listened album in the selected time period


def get_top_albums_fixed(data: Dict) -> List[AlbumFixed]:
    albums = []
    try:
        for i in (data["weeklyalbumchart"]["album"]):
            albums.append(AlbumFixed(i))

    except KeyError:
        print("Couldn't get link for {}")

    return albums


# prepares links for specified time period
def prepare_top_albums_links(start_date: datetime, time_delta: relativedelta, limit: int, end_date=datetime.now()) -> \
        Dict[datetime, str]:
    links = {}
    # "http://ws.audioscrobbler.com/2.0/?method=user.getweeklyalbumchart&user=heroesluk&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json&from={}&to={}".format(
    while start_date < end_date:
        link = "http://ws.audioscrobbler.com/2.0/?method=user.getweeklyalbumchart&user=heroesluk" \
               "&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json&from={}&to={}&limit={}". \
            format(int(start_date.timestamp()), int((start_date + time_delta).timestamp()), limit)

        start_date += time_delta

        links[start_date] = link

    return links

    # gets dict of favorite albums per specified time period


def fav_albums_per_timeperiod_json(start_date: datetime, time_delta: relativedelta, album_limit: int) -> Dict[
    datetime, Dict]:
    album_tops = {}
    cache = top_albums_dict()

    links = prepare_top_albums_links(start_date, time_delta, album_limit)
    session = FuturesSession(max_workers=20)
    futures = []
    for date, link in links.items():
        future = session.get(link)
        future.name = date
        futures.append(future)

    futures_dict = {}
    for future in as_completed(futures):
        futures_dict[future.name] = future.result().json()

    return futures_dict


def create_maxtrix(matrix_size, path, albums, date_key=None):
    # assume all images are same size
    try:
        album_size = albums[0].image.size[0]
    except AttributeError:
        print(albums)
    new_image = Image.new('RGB', (matrix_size * album_size, matrix_size * album_size), (250, 250, 250))

    index = 0
    for x in range(matrix_size):
        for y in range(matrix_size):
            try:
                new_image.paste(albums[index].image, (album_size * x, album_size * y))
                index += 1
            except IndexError:
                pass

    new_image.save("{}/mosaic_{}.jpg".format(path, date_key), "JPEG")

    return new_image


#create gif with albumgrid images sorted by date
def create_gif(images_dict):
    paths = list(sorted(["GIF/{}".format(i) for i in os.listdir("GIF") if "mosaic" in i]))
    fp_out = "image.gif"
    if fp_out in os.listdir():
        os.remove(fp_out)

    imgs: List[Image.Image] = list(images_dict.values())

    imgs[0].save("GIF/tak.gif", save_all=True, append_images=imgs[1:], optimize=False, loop=0, duration=400)



deltas = {"week": relativedelta(weeks=+1), "month": relativedelta(months=+1), "3month": relativedelta(months=+3),
          "6month": relativedelta(months=+6), "year": relativedelta(months=+12)}


def get_record_name(album: AlbumFixed) -> str:
    return sanitize_filename(album.artist + "_" + album.album_name)


def get_required_images_links(_top_albums_per_timeperiod: Dict[datetime, List[AlbumFixed]]) -> Dict[str, str]:
    records = set()

    for date, albums in _top_albums_per_timeperiod.items():
        for album in albums:
            # print(get_record_name(album))

            # sanitize it, since it will also work as a filename after downloading
            records.add(get_record_name(album))

    cache = top_albums_images()
    links_to_manually_download = []

    links_to_down = {}
    for record in records:
        if record in cache.keys():
            links_to_down[record] = cache[record]
        else:
            links_to_manually_download.append(record)

    links_to_down.update(get_img_links_manually(links_to_manually_download))

    return links_to_down


def download_batch_imgs(links: Dict[str, str]) -> Dict[str, Image.Image]:
    session = FuturesSession(max_workers=20)

    skipped = 0
    futures = []
    print(links)
    for record, link in links.items():

        if len(link) > 0:
            future = session.get(link)
            future.name = record
            futures.append(future)

    imgs_data = {}
    for future in as_completed(futures):
        try:
            resp = future.result()

            if resp.ok:
                f = io.BytesIO(resp.content)
                imgs_data[future.name] = Image.open(f)

            else:
                print("couldnt download {}".format(future.name))
        except requests.exceptions.MissingSchema:
            print(future, future.name)

    return imgs_data


# album is in format of artist_albumname
def get_img_links_manually(albums: List[str]) -> Dict[str, str]:
    links = {}
    for album in albums:
        artist, album_name = album.split('_')
        links[album] = ("http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_"
                        "key=d6e02ae58fcf6daaea788ce99c879f9c&artist={}&album={}&format=json".format(artist,
                                                                                                     album_name))

    session = FuturesSession(max_workers=20)
    futures = []

    for album, link in links.items():
        future = session.get(link)
        future.name = album
        futures.append(future)

    futures_dict = {}
    for future in as_completed(futures):
        temp = future.result().json()
        futures_dict[future.name] = temp['album']['image'][3]['#text']

    return futures_dict


def gif_creator(start_date: datetime, delta: str, matrix_size: int, end_date: datetime = None):
    time_delta = deltas[delta]
    top_albums_per_timeperiod_json = fav_albums_per_timeperiod_json(start_date, time_delta, 18)
    top_albums_per_timeperiod = {}
    for date, _json in top_albums_per_timeperiod_json.items():
        top_albums_per_timeperiod[date] = get_top_albums_fixed(_json)

    links = get_required_images_links(top_albums_per_timeperiod)
    imgs_data = download_batch_imgs(links)

    # imgs = [i for i in os.listdir("GIF")]

    matrixes = {}
    for date in sorted(top_albums_per_timeperiod.keys()):
        albums: List[AlbumFixed] = top_albums_per_timeperiod[date]
        for album in albums:
            try:
                album.image = imgs_data[get_record_name(album)]
            except KeyError:
                print("No image for album {}".format(album.album_name))

        temp = create_maxtrix(4, "GIF", [album for album in albums if album.image],
                       date_key=date)

        matrixes[date]: Dict[datetime, Image.Image] = temp

    create_gif(matrixes)


gif_creator(datetime(2022, 6, 1), "month", 4), datetime(2022, 12, 1)

# cProfile.run('gif_creator(datetime(2022, 6, 1), "month", 4), datetime(2022,12,1)')
# try to further optimize it
# add date banner
# flask app instead of script
# deploy as docker image on heroku


print(len(os.listdir("GIF")))
