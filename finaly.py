import requests, json
from xml.sax import parseString
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest

from itertools import count
import matplotlib.pyplot as plt
import sqlite3
import numpy as np


from sqlalchemy import values

from grammys import get_links


def make_request(song_lst): 
    matches = []
    songs = []
    for item in song_lst:
        song = item['song']
        artist = item['artist']
        year = item['year']
        r = requests.get("https://itunes.apple.com/search", params = {'term': song,
                                            'media': 'music'})
        result = json.loads(r.text)
        for info in result['results']:
            if info['artistName'] == artist and info['trackName'] == song and info['kind'] == 'song' and (year in info['releaseDate']):
                if song in songs:
                    continue
                else:
                    songs.append(song)
                    album = info['collectionName']
                    releasedate = info['releaseDate']
                    country = info['country']
                    genre = info['primaryGenreName']
                    full_song_data = {}
                    full_song_data['song'] = song
                    full_song_data['album'] = album
                    full_song_data['album'] = album
                    full_song_data['releasedate'] = releasedate
                    full_song_data['country'] = country
                    full_song_data['genre'] = genre
                    matches.append(full_song_data)
    return matches

def get_song_data(database): #the db that macey made 
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ database)
    cur = conn.cursor()
    cur.execute("""
    SELECT songdata.songtitle, songdata.year, artist.artistname
    FROM songdata
    JOIN artist
    ON songdata.artistid = artist.id
    """)
    data = cur.fetchall()
    #pulled from the database, got the data 

    data_lst = []
    for item in data:
        song_dict = {}
        song_dict['song'] = item[0]
        song_dict['artist'] = item[2]
        song_dict['year'] = item[1]
        data_lst.append(song_dict)
    return data_lst

def createDatabase(db_name):
   path = os.path.dirname(os.path.abspath(__file__))
   conn = sqlite3.connect(path+'/'+db_name)
   cur = conn.cursor()
   return cur, conn


#create table for artist and artistid
def create_genre_table(matches):
   cur, conn = createDatabase('artists.db')
   cur.execute("CREATE TABLE IF NOT EXISTS genres (genreid INTEGER UNIQUE PRIMARY KEY, genre STRING)")
   genres = []
   for match in matches:
       genre = match['genre']
       if genre not in genres:
           genres.append(genre)

   for i in range(len(genres)):
       cur.execute("INSERT INTO genres (genreid, genres) VALUES (?,?)",(i, genres[i]))
       conn.commit()

songs = get_links()
matches = make_request(songs)
print(matches)
   

 











# def make_plot_a(matches): #take matches from above 
#     #frequencies of the genres 
#     genre_count = {}
#     for match in matches:
#         genre = match['genre']
#         if genre in genre_count:
#             genre_count[genre] += 1
#         else:
#             genre_count[genre] = 1

#     #set up plot making 
#     my_lables = list(genre_count.keys())
#     values = np.array(list(genre_count.values()))

    

#     #print(values,lables)
#     #what is going on with pie charts 
#     plt.pie(values,my_lables)
#     plt.show()


    #return_lst = result['results']

# sample = [{'song': 'You Belong With Me', 'artist': 'Taylor Swift', 'year': '2008'}]
# print(make_request(sample))

# match = [{'song': 'You Belong With Me', 'album': 'Fearless', 'releasedate': '2008-11-11T12:00:00Z', 'country': 'USA', 'genre': 'Country'}, {'song': 'You Belong With Me', 'album': 'Fearless (Platinum Edition)', 'releasedate': '2008-11-11T12:00:00Z', 'country': 'USA', 'genre': 'Country'}, {'song': 'You Belong With Me', 'album': '2010 Grammy Nominees', 'releasedate': '2008-11-11T12:00:00Z', 'country': 'USA', 'genre': 'Pop'}]

# make_plot_a(match)