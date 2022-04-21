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
   url = 'https://en.wikipedia.org/wiki/Grammy_Award_for_Song_of_the_Year'
   request = requests.get(url)
   soup = BeautifulSoup(request.content, "html.parser")
   tables = soup.find_all('table')
   #print(type(tables))
   #print(tables)
   results = []
   count = 0
   for item in tables[1:9]:
       table = item.find("tbody")
       body = table.find_all('tr')
       #print(table)
       for row in body:
           #print(row)
           year_test = row.find('a', class_ = "mw-redirect")
           if year_test:
               year = row.find('a', class_ = "mw-redirect").text.strip()
               cells = item.find_all('td')
               results_lst = {}
               results_lst['Song Title'] = cells[1].text.strip()
               results_lst['Artist'] = cells[2].text.strip()
               results_lst['Year'] = year
               results.append(results_lst)
           else:
               continue
   print(results)
 
# Creating database
def createDatabase(db_name):
   path = os.path.dirname(os.path.abspath(__file__))
   conn = sqlite3.connect(path+'/'+db_name)
   cur = conn.cursor()
   return cur, conn
 
#create table for artist and artistid
def create_artist_table(cur, conn):
   cur.execute("CREATE TABLE IF NOT EXISTS artists (artistid INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL, artistname STRING")
   conn.commit()
 
#if we do use the increment thing
def insert_artistsdata(results, cur, conn):
   all_artists = results['Artist']
   for artistname in all_artists:
       cur.execute("INSERT OR IGNORE INTO artists (artistid, artistname) VALUES (?, ?)" (artistid, artistname))
      
 
#insert artist info into table if we dont do the increment thing
def insert_artistsdata(results, cur, conn):
   artist_names = list(results['Artist'])
   artist_dic = {}
   artistid = 1
   for artistname in artist_names:
       if artistname not in artist_dic:
           artistid += 1
       artist_dic[artistname] = artistid
  
   cur.execute("INSERT OR IGNORE INTO artists (artistid, artistname) VALUES (?, ?)" (artistid, artistname))
   conn.commit()
 
 
#create table for grammy songs of the year
def create_songdata_table(cur, conn):
   cur.execute("CREATE TABLE IF NOT EXISTS songdata (entryid INTEGER UNIQUE PRIMARY KEY IDENTITY (1,1), songtitle STRING, year INTEGER, artistid INTEGER")
   conn.commit()
 
def insert_songdata(results, cur, conn):
   for lst in results:
       songtitle = lst['Song']
       year = lst['Year']
       cur.execute("INSERT OR IGNORE INTO songdata(songtitle, year, artistid) VALUES (?, ?, ?, ?)"(songtitle, year, #artistid???))
       conn.commit()
 
 
 
#get_links()
