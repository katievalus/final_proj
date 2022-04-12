import requests, json
from xml.sax import parseString
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest

def get_links(): #this should be good 
    url = 'https://en.wikipedia.org/wiki/Grammy_Award_for_Song_of_the_Year'
    request = requests.get(url)
    soup = BeautifulSoup(request.content, "html.parser")
    tables = soup.find_all('tr')
    print(type(tables))
    #print(tables)
    results = []
    for item in tables:
        text = item.get('th')
        print(text)
        #resutls = {}
        #print(type(item.text))
        #results["year"] = item[0]
        

get_links()