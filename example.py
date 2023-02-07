import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Tuple, Dict
import os
import imageio
from PIL import Image



#i want to display every album per month

class TimeStamp:
    def __init__(self, start: str, end: str):
        self.start = int(start)
        self.end = int(end)

        self.start_date = datetime.fromtimestamp(self.start)
        self.month = self.start_date.month
        self.year = self.start_date.year


    def time_stamp(self):
        return str(self.start), str(self.end)

def get_cache_album_data():
    data = requests.get(
        "http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&use"
        "r=Heroesluk&limit=500&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json").json()


    return  {i['url']:i for i in data['topalbums']['album']}


class Album():
    def __init__(self, data, rank_context=None):
        self.artist = data['artist']['#text']
        self.album_name = data['name']
        self.url = data['url']

        self.rank = int(data["@attr"]['rank'])
        self.play_count = int(data['playcount'])

        self.image = None
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

            self.image = data['album']['image'][3]['#text']

        if len(self.image)==0:
            print("Couldnt find image for {}".format(self.album_name))








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

        if len(albums)>top:
            return albums


    return albums


# gets dict of favorite albums per specified time period
# i.e {month1:[Album1, Album2], month2:[Album4, Album1]} etc
def get_list_of_fav_artists(start_date: datetime, time_delta: relativedelta, albums_per_delta: int):

    album_tops = {}
    cache = get_cache_album_data()

    while start_date<datetime.now():
        albums = get_top_albums(int(start_date.timestamp()),int((start_date+time_delta).timestamp()),albums_per_delta)
        print("Top for: {}".format(start_date))

        album_tops[start_date] = []
        for album in albums:


            album.load_more_metadata(cache)
            album.print_out()
            album_tops[start_date].append(album)

        start_date+=time_delta
        print("\n"*3)



    return album_tops




# for k,v in data.items():
#     print(k, [i.image for i in v ])

#will save images as i.e 10_2022_INDEX where index is incrementing
def download_images(image_links, key_name) -> list:
    data = []
    name = 1
    for link in image_links:
        with open("GIF/{}_{}.jpg".format(key_name,name), 'wb') as f:
            data_img = requests.get(link).content
            f.write(data_img)
            name+=1

    return ["GIF/{}".format(i) for i in os.listdir("GIF")]


# # albums1 = data[datetime(2022,11,1)]
# links = [i.image for i in albums1]
#
# paths = download_images(links, datetime(2022,11,1).strftime("%m-%Y"))




def create_maxtrix(matrix_size, path, date_key=None):
    #for now assume all images are same size
    #assuming album is Z times Z size
    albums = [Image.open('{}/{}'.format(path, i)) for i in os.listdir(path) if date_key in i]

    album_size =  albums[0].size[0]

    new_image = Image.new('RGB', (matrix_size *album_size, matrix_size * album_size), (250, 250, 250))

    index = 0
    for x in range(matrix_size):
        for y in range(matrix_size):
            new_image.paste(albums[index], (album_size*x, album_size*y))
            index+=1

    new_image.save("{}/mosaic_{}.jpg".format(path,date_key), "JPEG")



start = datetime(2022,11,1)
data = get_list_of_fav_artists(start,relativedelta(months=+1),9)

for date, albums_per_date in data.items():
    print(date)

    albums = data[date]
    album_img_links = [i.image for i in albums]
    paths = download_images(album_img_links, date.strftime("%m-%Y"))
    create_maxtrix(3, 'GIF', date.strftime("%m-%Y"))




def create_gif():
    paths = list(sorted(["GIF/{}".format(i) for i in os.listdir("GIF") if "mosaic" in i]))
    print(paths)
    fp_out = "image.gif"
    images = []
    for file_name in paths:
        images.append(imageio.imread(file_name))

    imageio.mimsave('movie.gif', images, fps=1)


create_gif()






