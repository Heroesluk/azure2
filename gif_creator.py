import cProfile
from concurrent.futures import as_completed
from pathvalidate import sanitize_filename

import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import List, Dict
from PIL import Image
from requests_futures.sessions import FuturesSession
import io

files = []


def clean_up():
    from pathlib import Path

    [f.unlink() for f in Path("GIF").glob("*") if f.is_file()]


class Album():

    def __init__(self, data):
        self.artist = data['artist']['#text']
        self.album_name = data['name']
        self.url = data['url']
        self.rank = int(data["@attr"]['rank'])
        self.play_count = int(data['playcount'])
        self.image_path = get_record_name(self)
        self.image = None


def get_top_albums_list(data: Dict) -> List[Album]:
    albums = []
    try:
        for i in (data["weeklyalbumchart"]["album"]):
            albums.append(Album(i))

    except KeyError:
        print("Couldn't get link for {}")

    return albums


# prepares links for specified time periods, example link looks like:
# http://ws.audioscrobbler.com/2.0/?
# method=user.getweeklyalbumchart&user={usr}&api_key={key}&format=json&from={}&to={}
def prepare_timeperiod_album_requests(start_date: datetime, time_delta: relativedelta,
                                      limit: int, end_date=datetime.now()) -> Dict[datetime, str]:
    links = {}
    while start_date < end_date:
        link = "http://ws.audioscrobbler.com/2.0/?method=user.getweeklyalbumchart&user=heroesluk" \
               "&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json&from={}&to={}&limit={}". \
            format(int(start_date.timestamp()), int((start_date + time_delta).timestamp()), limit)

        start_date += time_delta

        links[start_date] = link

    return links


# gets dict of favorite albums per specified time as json
# using https://www.last.fm/api/show/user.getWeeklyAlbumChart
def fav_albums_per_timeperiod_json(start_date: datetime, time_delta: relativedelta,
                                   album_limit: int, end_date: datetime = None) -> Dict[datetime, Dict]:
    links = prepare_timeperiod_album_requests(start_date, time_delta, album_limit)
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

    album_size = albums[0].image.size[0]
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





def get_record_name(album: Album) -> str:
    return sanitize_filename(album.artist + "_" + album.album_name)


# since lastfm weeklychart doesn't give us links
# to album covers ( or rather, it gives empty fields )
# we have to cheat a bit
def top_albums_images():
    data = requests.get(
        "http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&use"
        "r=Heroesluk&limit=500&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json").json()

    return {sanitize_filename(i['artist']['name'] + "_" + i['name']): i['image'][3]['#text'] for i in
            data['topalbums']['album']}


# to avoid requesting album.getInfo for every album, create temporary cache consiting of all-time most
# listened to albums, if needed album is not in it, only then request it manually
# there's a chance for bigger gifs, with longer time periods, extending the cache from 500 to more albums
# could improve performance
def get_required_images_links(_top_albums_per_timeperiod: Dict[datetime, List[Album]]) -> Dict[str, str]:
    records = set()
    cache = top_albums_images()
    links_to_manually_download = []

    for date, albums in _top_albums_per_timeperiod.items():
        for album in albums:
            # record_name corresponds to artistName_albumTitle
            records.add(get_record_name(album))

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

    futures = []
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
                print("couldn't download {}".format(future.name))
        except requests.exceptions.MissingSchema:
            print(future, future.name)

    return imgs_data


def get_img_links_manually(albums: List[str]) -> Dict[str, str]:
    links = {}
    # record is in format of artistName_albumName
    for record in albums:
        artist, album_name = record.split('_')
        links[record] = ("http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_"
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


# create gif with albumgrid images sorted by date
def create_gif(images_dict, file_name):
    imgs: List[Image.Image] = list(images_dict.values())

    imgs[0].save("static/{}.gif".format(file_name), save_all=True, append_images=imgs[1:], optimize=False, loop=0, duration=400)

    return imgs[0]


def gif_creator(start_date: datetime, delta: str, matrix_size: int, file_name: str, end_date: datetime = None):
    deltas = {"week": relativedelta(weeks=+1), "month": relativedelta(months=+1), "3month": relativedelta(months=+3),
              "6month": relativedelta(months=+6), "year": relativedelta(months=+12)}
    time_delta = deltas[delta]

    top_albums_per_timeperiod_json = fav_albums_per_timeperiod_json(start_date,
                                                                    time_delta,
                                                                    (matrix_size * matrix_size) + 2)

    # create dict where key is date, and value is list of Album instances
    # corresponding to most listened to albums for specified time period
    top_albums_per_timeperiod = {}
    for date, _json in top_albums_per_timeperiod_json.items():
        top_albums_per_timeperiod[date] = get_top_albums_list(_json)

    # extract required links and download album covers to memory
    links = get_required_images_links(top_albums_per_timeperiod)
    imgs_data = download_batch_imgs(links)

    # prepare album mosaics for every timeperiod
    matrixes = {}
    for date in sorted(top_albums_per_timeperiod.keys()):
        albums: List[Album] = top_albums_per_timeperiod[date]
        for album in albums:
            try:
                album.image = imgs_data[get_record_name(album)]
            except KeyError:
                print("No image for album {}".format(album.album_name))

        temp = create_maxtrix(matrix_size, "GIF", [album for album in albums if album.image],
                              date_key=date)

        matrixes[date]: Dict[datetime, Image.Image] = temp

    return create_gif(matrixes, file_name)



