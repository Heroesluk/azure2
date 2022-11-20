import sqlite3
import json, time
import os


def parse_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    data_p = []

    for i in data:
        data_p.append((i['name'], i['artist']['name'],
                       i['image'][0]['#text'], i['image'][1]['#text'], None))

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


import sqlite3

def readSqliteTable():
    try:
        sqliteConnection = sqlite3.connect('albums.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from AlbumList"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")


        album_dict = {row[0]:row[3] for row in records}
        # for row in records:
        #     print("Id: ", row[0])
        #     print("Album: ", row[1])
        #     print("Artist: ", row[2])
        #     print("Link: ", row[3])
        #     print("LinkBig: ", row[4])
        #     print("Img: ", row[5])
        #     print("\n")

        cursor.close()

        return album_dict


    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def select_from_id_list(data):
    data = [(i.split('.')[0],) for i in data]
    records = []
    sqlite_select_query = """SELECT ID, big_img_link from AlbumList 
        WHERE ID=?"""
    sqliteConnection = sqlite3.connect('albums.db')
    cursor = sqliteConnection.cursor()

    for i in data:
        cursor.execute(sqlite_select_query,i )
        records += cursor.fetchall()

    return records


#[400:420]
#select_from_id_list(_data)

