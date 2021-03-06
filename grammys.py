from operator import index
import requests, json
from xml.sax import parseString
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import sqlite3
import json
import os
 
 
def get_links():
   url = 'https://top40weekly.com/top-100-songs-of-all-time/'
   request = requests.get(url)
   soup = BeautifulSoup(request.content, "html.parser")
   song_scrape = soup.find_all('div', class_ = 'x-text song-title')
   artist_scrape = soup.find_all('div', class_ = 'x-text artist-name')
   year_scrape = soup.find_all('div', class_ = 'x-text song-rel')
   songs = []
   #artists = []
   for index in range(len(song_scrape)):
       a = (song_scrape[index])
       b = (artist_scrape[index])
       c = (year_scrape[index])
       song = a.text.strip()
       artist = b.text.strip()
       year = c.text.strip()
       
       index +=1
       tup = (song,artist,year[-4:])
       songs.append(tup)
   return songs



# Creating database
def createDatabase(db_name):
   path = os.path.dirname(os.path.abspath(__file__))
   conn = sqlite3.connect(path+'/'+db_name)
   cur = conn.cursor()
   return cur, conn


#create table for artist and artistid
def create_artist_table(artistnames):
   cur, conn = createDatabase('artists.db')
   cur.execute("CREATE TABLE IF NOT EXISTS artists (artistid INTEGER UNIQUE PRIMARY KEY, artistname STRING)")

   for i in range(len(artistnames)):
      print(i)
      print(artistnames[i])
      cur.execute("INSERT INTO artists (artistid, artistname) VALUES (?,?)",(i, artistnames[i]))
      conn.commit()

 
# gets a list of artists only once 

def get_artistnames(data):
   artist_lst = []
   for result in data:
      if result[1] in artist_lst:
         continue
      else:
         artist_lst.append(result[1])
   return artist_lst

#loop over the len of the list 
#index is the id and the item is the name 
   #set text as primary key 
   #TEXT PRIMARY KEY -- artist name 
   #Insert or Ignore into -- prevents duplicates 


 
#create table for top 100 songs of all time
# def create_songdata_table(cur, conn):
#    cur.execute("CREATE TABLE IF NOT EXISTS songdata (entryid INTEGER UNIQUE PRIMARY KEY IDENTITY, songtitle STRING, year INTEGER, artistid INTEGER")
#    conn.commit()
 
# def insert_songdata(results, cur, conn):
#    for lst in results:
#        songtitle = lst['Song']
#        year = lst['Year']
#        cur.execute("INSERT OR IGNORE INTO songdata(songtitle, year, artistid) VALUES (?, ?, ?, ?)"(songtitle, year, artistid))
#        conn.commit()
 
 


def main():
   songinfo = get_links() 
   artistnames = get_artistnames(songinfo)
   create_artist_table(artistnames)


main()




