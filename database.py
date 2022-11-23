import sqlite3
import json, time
import os
from typing import List
import requests


def create_albums_json(user: str, number_of_albums_times_500: int, path: str):
    concentrate = []
    # divide request since lastfm api response breaks when requesting more then 500 albums per page
    for page in range(1, number_of_albums_times_500 + 1):
        try:
            data = requests.get(
                'http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&limit=500&page={}&user={}&api_key=d6e02ae58fcf6daaea788ce99c879f9c&format=json'.format(
                    page, user))
            data.raise_for_status()

            concentrate.append(data.json())
        except requests.exceptions.HTTPError as error:
            print(error)
            return

    # merge json files from memory into one
    head = concentrate[0]['topalbums']['album']
    for i in concentrate[1:]:
        head += i['topalbums']['album']

    with open(path, 'w') as f:
        json.dump(head, f)


def parse_json(path): # load parse data, before passing it to database
    with open(path, 'r') as file:
        data = json.load(file)
    data_p = []

    for i in data:
        data_p.append((i['name'], i['artist']['name'],
                       i['image'][0]['#text'], i['image'][2]['#text'], None))

    return data_p


def insert_data(_data):
    sqlite_insert_query = """INSERT INTO AlbumList
                          (album_name, artist_name, small_img_link, big_img_link, small_img) 
                           VALUES 
                          (?, ?, ?, ?, ?);"""

    con = sqlite3.connect('albums.db')

    con.executemany(sqlite_insert_query, _data)
    con.commit()
    con.close()


def read_rows(cols_to_fetch: list = (0, 1, 0, 0, 0, 0,)) -> List[tuple]:
    try:
        sqliteConnection = sqlite3.connect('albums.db')

        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from AlbumList"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))

        # return values only from "1" rows
        albums = [tuple(v for i, v in enumerate(row) if cols_to_fetch[i]) for row in records]
        #print(album_dict)
        # for row in records:
        #     print("Id: ", row[0])
        #     print("Album: ", row[1])
        #     print("Artist: ", row[2])
        #     print("Link: ", row[3])
        #     print("LinkBig: ", row[4])
        #     print("Img: ", row[5])
        #     print("\n")

        cursor.close()

        return albums


    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


# id directly coresponds to filenames in AlbumCovers
def select_from_id_list(data):
    data = [(i.split('.')[0],) for i in data]
    records = []
    sqlite_select_query = """SELECT ID, big_img_link from AlbumList 
        WHERE ID=?"""
    sqliteConnection = sqlite3.connect('albums.db')
    cursor = sqliteConnection.cursor()

    for i in data:
        cursor.execute(sqlite_select_query, i)
        records += cursor.fetchall()

    return records


def clear_table():
    conn = sqlite3.connect('albums.db')
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM AlbumList""")
    conn.commit()
    conn.close()

data = parse_json('albums1.json')

insert_data(data)

#create_albums_json('heroesluk',5,'albums1.json')

# [400:420]
# select_from_id_list(_data)
for i in read_rows():
    print(i)
