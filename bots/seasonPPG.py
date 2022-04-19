# 10 highest ppg of current season
from tkinter.tix import INTEGER
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import contextlib

# database connection
conn = sqlite3.connect('my_database.db')
cur = conn.cursor()

#url I'm scraping
url = "https://www.basketball-reference.com/leagues/NBA_2022_per_game.html#per_game_stats::pts_per_g"

# url = "https://www.basketball-reference.com/playoffs/"
# collect html data
html = urlopen(url)
#create beautiful soup object from HTML
soup = BeautifulSoup(html, 'html.parser')

# collect info from table header 
headers = [th.getText() for th in soup.findAll('tr') 
[0].findAll('th')]
headers = headers[1:]
headers = ["field1", "field2", "field3"]
print(headers)


#  GENERAL Table
cur.execute('DROP TABLE IF EXISTS GENERAL')
cur.execute('''CREATE TABLE GENERAL 
            (Player text, Pos text, Age INTEGER, Tm text, G INTEGER, GS INTEGER, MP real)''')
conn.commit()
cur.execute('SELECT * FROM GENERAL')
print(f'this is general table: {cur.fetchall()}')

# BOFF Table
cur.execute('DROP TABLE IF EXISTS BOFF')
cur.execute('''CREATE TABLE BOFF 
            (FG real, FGA real, 3P real, 3PA real, 2P real, 2PA real, FT real, FTA real, AST real, PTS real)''')
conn.commit()
cur.execute('SELECT * FROM BOFF')
print(f'this is BOFF table: {cur.fetchall()}')

# AOFF Table
cur.execute('DROP TABLE IF EXISTS AOFF')
cur.execute('''CREATE TABLE AOFF 
            (FGP real, 3PP real, 2PP real, eFGP real, FTP real)''')
conn.commit()
cur.execute('SELECT * FROM AOFF')
print(f'this is AOFF table: {cur.fetchall()}')

# DEF Table
cur.execute('DROP TABLE IF EXISTS DEF')
cur.execute('''CREATE TABLE DEF 
            (STL real, BLK real, TOV real, PF real)''')
conn.commit()
cur.execute('SELECT * FROM DEF')
print(f'this is DEF table: {cur.fetchall()}')

# OTHER Table
cur.execute('DROP TABLE IF EXISTS OTHER')
cur.execute('''CREATE TABLE AOFF 
            (ORB real, DRB real, TRB real, PF real)''')
conn.commit()
cur.execute('SELECT * FROM OTHER')
print(f'this is OTHER table: {cur.fetchall()}')


#get rows from table
rows = soup.findAll('tr')[2:]
rows_data = [[td.getText() for td in rows[i].findAll('td')] 
for i in range(len(rows))]
rows_data = rows_data[0:38]
rows_data = ["field1", "field2", "field3"]
cur.close()
conn.close()

# #dataframe
# player_stats = pd.DataFrame(rows_data, columns=headers)

# #export to CSV
# player_stats.to_csv("players_stats.csv", index=False, sep=";")