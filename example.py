import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Tuple, Dict
import os
import imageio
from PIL import Image

files = []


def convert_last_album_cover_link_to_id(link: str):
    return (link.split("/")[-1]).split('.jpg')[0]


def get_cache_album_data():
    data = requests.get(
        "http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&use"
        "r=Heroesluk&limit=500&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json").json()

    return {i['url']: i for i in data['topalbums']['album']}


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
    for i in (data["weeklyalbumchart"]["album"]):
        albums.append(Album(i))

        if len(albums) > top:
            return albums

    return albums


# gets dict of favorite albums per specified time period
# i.e {month1:[Album1, Album2], month2:[Album4, Album1]} etc
def get_list_of_fav_artists(start_date: datetime, time_delta: relativedelta, matrix_size: int):
    album_tops = {}
    cache = get_cache_album_data()

    while start_date < datetime.now():
        albums = get_top_albums(int(start_date.timestamp()), int((start_date + time_delta).timestamp()),
                                matrix_size * matrix_size)
        print("Top for: {}".format(start_date))

        album_tops[start_date] = []
        for album in albums:
            album.load_more_metadata(cache)
            album.print_out()
            # append only if image exists
            if album.image:
                album_tops[start_date].append(album)

        start_date += time_delta
        print("\n" * 3)

    return album_tops


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

    imageio.mimsave('movie.gif', images, fps=1)


def gif_creator(start_date: datetime, delta: relativedelta, matrix_size: int, end_date: datetime = None):
    data = get_list_of_fav_artists(start_date, delta, matrix_size)

    for date, albums_per_date in data.items():
        albums = data[date]
        album_file_names = [i.image_path for i in albums]
        create_maxtrix(matrix_size, 'GIF', album_file_names, date.strftime("%Y-%m"))

    create_gif()


#gif_creator(datetime(2020, 1, 1), relativedelta(months=+3), 3)

# try to further optimize it
# add date banner
# flask app instead of script
# deploy as docker image on heroku
