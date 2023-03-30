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




class Album():
    def __init__(self, data, rank_context=None):
        self.artist = data['artist']['#text']
        self.album_name = data['name']
        self.url = data['url']

        self.rank = int(data["@attr"]['rank'])
        self.play_count = int(data['playcount'])

        self.image = None
        self.image_path = None
        self.tags = []

    def print_out(self):
        print("{}. {} by {} played {} times".format(self.rank, self.album_name, self.artist, self.play_count))

    def load_more_metadata(self, cache: dict):
        if self.url in cache.keys():
            try:
                self.image = cache[self.url]['image'][3]['#text']

            except KeyError:
                print("Couldn't find image for {} in cache, running request for image".format(self.album_name))

        else:
            print("Getting request")
            data = requests.get(
                "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=d6e02ae58fcf6daaea788ce99c879f9c&artist={}&album={}&format=json".format(
                    self.artist, self.album_name)).json()
            #
            # for tag in data['album']['tags']['tag']:
            #     self.tags.append(tag['name'])
            try:
                self.image = data['album']['image'][3]['#text']
            except KeyError:
                print("Couldn't find image for {} with request".format(self.album_name))

        if self.image:
            self.download_image()

    def download_image(self):
        global files

        file_name = convert_last_album_cover_link_to_id(self.image)

        if file_name in files:
            self.image_path = file_name
        else:
            if ("GIF" not in os.listdir()):
                os.mkdir("GIF")

            with open("GIF/{}.jpg".format(file_name), 'wb') as f:
                data_img = requests.get(self.image).content
                f.write(data_img)

            files.append(file_name)
            self.image_path = file_name


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
def get_top_albums(start_date: int, end_date: int, top: int = 1000) -> List[Album]:
    data = requests.get(
        "http://ws.audioscrobbler.com/2.0/?method=user.getweeklyalbumchart&user=heroesluk&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json&from={}&to={}".format(
            start_date, end_date))

    data = data.json()
    albums = []
    try:
        for i in (data["weeklyalbumchart"]["album"]):
            albums.append(Album(i))

            if len(albums) > top:
                return albums
    except KeyError:
        print("Couldn't get link for {}".format(start_date))

    return albums


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


# i.e {month1:[Album1, Album2], month2:[Album4, Album1]} etc
# def get_list_of_fav_artists(start_date: datetime, time_delta: relativedelta, matrix_size: int, end_date=datetime.now()):
#     album_tops = {}
#     cache = top_albums_dict()
#
#     while start_date < end_date:
#         albums = get_top_albums(int(start_date.timestamp()), int((start_date + time_delta).timestamp()),
#                                 matrix_size * matrix_size)
#         print("Top for: {}".format(start_date))
#
#         album_tops[start_date] = []
#         for album in albums:
#             album.load_more_metadata(cache)
#             album.print_out()
#             # append only if image exists
#             if album.image:
#                 album_tops[start_date].append(album)
#
#         start_date += time_delta
#         print("\n" * 3)
#
#     return album_tops


# gets dict of favorite albums per specified time period
# i.e {month1:[Album1, Album2], month2:[Album4, Album1]} etc


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


def create_maxtrix(matrix_size, path, album_file_names, date_key=None):
    # assume all images are same size
    albums = [Image.open('{}/{}.jpg'.format(path, i)) for i in album_file_names]
    album_size = albums[0].size[0]
    new_image = Image.new('RGB', (matrix_size * album_size, matrix_size * album_size), (250, 250, 250))

    index = 0
    for x in range(matrix_size):
        for y in range(matrix_size):
            try:
                new_image.paste(albums[index], (album_size * x, album_size * y))
                index += 1
            except IndexError:
                pass

    new_image.save("{}/mosaic_{}.jpg".format(path, date_key), "JPEG")


def create_gif():
    paths = list(sorted(["GIF/{}".format(i) for i in os.listdir("GIF") if "mosaic" in i]))
    fp_out = "image.gif"
    if fp_out in os.listdir():
        os.remove(fp_out)

    images = []
    for file_name in paths:
        images.append(imageio.imread(file_name))

    imageio.mimsave('static/movie.gif', images, fps=1)


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


def download_batch_imgs(links: Dict[str, str]):
    session = FuturesSession(max_workers=20)

    futures = []
    for record, link in links.items():
        future = session.get(link)
        future.name = record
        futures.append(future)

    futures_dict = {}
    for future in as_completed(futures):
        resp = future.result()
        if (resp):
            with open('GIF/{}.png'.format(future.name), 'wb') as f:
                f.write(resp.content)
        else:
            print("couldnt download {}".format(future.name))


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
    top_albums_per_timeperiod_json = fav_albums_per_timeperiod_json(start_date, time_delta, 17)
    top_albums_per_timeperiod = {}
    for date, _json in top_albums_per_timeperiod_json.items():
        top_albums_per_timeperiod[date] = get_top_albums_fixed(_json)

    links = get_required_images_links(top_albums_per_timeperiod)
    download_batch_imgs(links)

    imgs = [i for i in os.listdir("GIF")]
    for date, albums in top_albums_per_timeperiod.items():
        for album in albums:
            if album.image_path + ".png" not in imgs:
                print(album.album_name, album.image_path)


    # for date, albums_per_date in data.items():
    #     albums = data[date]
    #     album_file_names = [i.image_path for i in albums]
    #     create_maxtrix(matrix_size, 'GIF', album_file_names, date.strftime("%Y-%m"))
    #
    # create_gif()


gif_creator(datetime(2022, 6, 1), "month", 4), datetime(2022, 12, 1)

# cProfile.run('gif_creator(datetime(2022, 6, 1), "month", 4), datetime(2022,12,1)')
# try to further optimize it
# add date banner
# flask app instead of script
# deploy as docker image on heroku


print(len(os.listdir("GIF")))
