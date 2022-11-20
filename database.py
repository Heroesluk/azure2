import sqlite3
import json, time

sqlite_insert_query = """INSERT INTO AlbumList
                      (album_name, artist_name, small_img_link, big_img_link, small_img) 
                       VALUES 
                      (?, ?, ?, ?, ?);"""


def parse_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    data_p = []

    for i in data:
        data_p.append((i['name'], i['artist']['name'],
                       i['image'][0]['#text'], i['image'][1]['#text'], None))

    return data_p


data = parse_json('albums.json')
con = sqlite3.connect('albums.db')

# Fill the table
con.executemany(sqlite_insert_query, data)
con.commit()
con.close()
