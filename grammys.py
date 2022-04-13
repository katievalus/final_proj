import requests, json
from xml.sax import parseString
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest

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
                results_dic = {}
                results_dic['Song Title'] = cells[1].text.strip()
                results_dic['Artist'] = cells[2].text.strip()
                results_dic['Year'] = year
                results.append(results_dic)
            else:
                continue

    print(results)



        
        #print(type(item.text))
        #results["year"] = item[0]
        

get_links()