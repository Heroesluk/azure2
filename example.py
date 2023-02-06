import json

import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Tuple
from json import dump


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


class Album():
    def __init__(self, data, rank_context=None):
        self.artist = data['artist']['#text']
        self.album_name = data['name']

        self.rank = int(data["@attr"]['rank'])
        self.play_count = int(data['playcount'])


    def print_out(self):
        print("{}. {} by {} played {} times".format(self.rank, self.album_name, self.artist, self.play_count))

# returns list of most listened album in the selected time period
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





def get_list_of_fav_artists(start_date: datetime, time_delta: relativedelta):

    while start_date<datetime.now():
        albums = get_top_albums(int(start_date.timestamp()),int((start_date+time_delta).timestamp()),9)
        print("Top for: {}".format(start_date))
        for album in albums:
            album.print_out()
        start_date+=time_delta
        print("\n"*3)




get_list_of_fav_artists(datetime(2022,1,1),relativedelta(months=+1))






