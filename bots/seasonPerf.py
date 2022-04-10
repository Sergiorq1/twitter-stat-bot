# 10 highest game scores of current season
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

#url I'm scraping
url = "https://www.basketball-reference.com/leaders/game_score.html#stats_game_game_score"
#collect html data
html = urlopen(url)
#create beautiful soup object from HTML
soup = BeautifulSoup(html, 'html.parser')

headers = [th.getText() for th in soup.findAll('tr', limit=2) 
[0].findAll('th')]
print(headers)