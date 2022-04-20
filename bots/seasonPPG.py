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

# collect html data
html = urlopen(url)
#create beautiful soup object from HTML
soup = BeautifulSoup(html, 'html.parser')

# collect info from table header 
headers = [th.getText() for th in soup.findAll('tr') 
[0].findAll('th')]
headers = headers[1:]
Gheaders = headers[:7]
BOFFindices = [7,8,10,11,13,14,17,18,23,28]
AOFFindices = [9,12,15,16,19]
DEFindices = [24,25]
OTHERindices = [20,21,22,26,27]
BOFFheaders = [headers[index] for index in BOFFindices]
print(BOFFheaders)
#  GENERAL Table
cur.execute('DROP TABLE IF EXISTS GENERAL')
cur.execute('''CREATE TABLE GENERAL 
            (Player text, Pos text, Age INTEGER, Tm text, G INTEGER, GS INTEGER, MP real)''')
cur.execute('INSERT INTO GENERAL VALUES(?,?,?,?,?,?,?)', Gheaders)
conn.commit()
cur.execute('SELECT * FROM GENERAL')
print(f'this is general table: {cur.fetchall()}')

# BOFF Table
cur.execute('DROP TABLE IF EXISTS BOFF')
cur.execute('''CREATE TABLE BOFF 
            (FG real, FGA real, 3P real, 3PA real, 2P real, 2PA real, FT real, FTA real, AST real, PTS real)''')
cur.execute('INSERT INTO GENERAL VALUES(?,?,?,?,?,?,?,?,?,?)', BOFFheaders)
conn.commit()
cur.execute('SELECT * FROM BOFF')
print(f'this is BOFF table: {cur.fetchall()}')

# # AOFF Table 
# cur.execute('DROP TABLE IF EXISTS AOFF')
# cur.execute('''CREATE TABLE AOFF 
#             (FGP real, 3PP real, 2PP real, eFGP real, FTP real)''')
# conn.commit()
# cur.execute('SELECT * FROM AOFF')
# print(f'this is AOFF table: {cur.fetchall()}')
Player;Pos;Age;Tm;G;GS;MP;FG;FGA;FG%; 103P; 113PA; 123P%;13 2P;14 2PA;15 2P%;16 eFG%;17 FT;18 FTA;FT%;ORB;DRB;TRB;23AST;STL;BLK;TOV;PF;28PTS

# # DEF Table 
# cur.execute('DROP TABLE IF EXISTS DEF')
# cur.execute('''CREATE TABLE DEF 
#             (STL real, BLK real)''')
# conn.commit()
# cur.execute('SELECT * FROM DEF')
# print(f'this is DEF table: {cur.fetchall()}')

# # OTHER Table 
# cur.execute('DROP TABLE IF EXISTS OTHER')
# cur.execute('''CREATE TABLE AOFF 
#             (ORB real, DRB real, TRB real, TOV real, PF real)''')
# conn.commit()
# cur.execute('SELECT * FROM OTHER')
# print(f'this is OTHER table: {cur.fetchall()}')


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