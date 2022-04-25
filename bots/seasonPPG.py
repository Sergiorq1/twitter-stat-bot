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
url = "https://www.basketball-reference.com/leagues/NBA_2022_per_game.html"

# collect html data
html = urlopen(url)
#create beautiful soup object from HTML
soup = BeautifulSoup(html, 'html.parser')

# collect info from table header 
headers = [th.getText() for th in soup.findAll('tr') 
[0].findAll('th')]
headers = headers[1:]
Gheaders = headers[:7]
Gindices = [0,1,2,3,4,5,6]
BOFFindices = [7,8,10,11,13,14,17,18,23,28]
AOFFindices = [9,12,15,16,19]
DEFindices = [24,25]
OTHERindices = [20,21,22,26,27]
BOFFheaders = [headers[index] for index in BOFFindices]
AOFFheaders = [headers[index] for index in AOFFindices]
DEFheaders = [headers[index] for index in DEFindices]
OTHERheaders = [headers[index] for index in OTHERindices]
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
            (FG real, FGA real, THP real, THPA real, TWOP real, TWOPA real, FT real, FTA real, AST real, PTS real)''')
cur.execute('INSERT INTO BOFF VALUES(?,?,?,?,?,?,?,?,?,?)', BOFFheaders)
conn.commit()
cur.execute('SELECT * FROM BOFF')
print(f'this is BOFF table: {cur.fetchall()}')

# AOFF Table 
cur.execute('DROP TABLE IF EXISTS AOFF')
cur.execute('''CREATE TABLE AOFF 
            (FGP real, THPP real, TWOPP real, eFGP real, FTP real)''')
cur.execute('INSERT INTO AOFF VALUES(?,?,?,?,?)', AOFFheaders)
conn.commit()
cur.execute('SELECT * FROM AOFF')
print(f'this is AOFF table: {cur.fetchall()}')

# DEF Table 
cur.execute('DROP TABLE IF EXISTS DEF')
cur.execute('''CREATE TABLE DEF 
            (STL real, BLK real)''')
cur.execute('INSERT INTO DEF VALUES(?,?)', DEFheaders)
conn.commit()
cur.execute('SELECT * FROM DEF')
print(f'this is DEF table: {cur.fetchall()}')

# OTHER Table 
cur.execute('DROP TABLE IF EXISTS OTHER')
cur.execute('''CREATE TABLE OTHER 
            (ORB real, DRB real, TRB real, TOV real, PF real)''')
cur.execute('INSERT INTO OTHER VALUES(?,?,?,?,?)', OTHERheaders)
conn.commit()
cur.execute('SELECT * FROM OTHER')
print(f'this is OTHER table: {cur.fetchall()}')


#get rows from table
rows = soup.findAll('tr', class_='full_table')

# rows_data = [[td.getText() for td in rows[i].findAll('td')]
# for i in range(len(rows))]
# rows_data = rows_data[:38]
# print(rows_data)
listting = []
# G_rows_data = [[G_rows_data.append(rows[i].find('td')[td])] for td, i in zip(Gindices, range(len(rows)))]

#collecting 'GENERAL' data from table 
for i in range(len(rows)):
    for td in Gindices:
        listting.append(rows[i].findAll('td')[td].getText())

# G_rows_data = [[td.getText() for td in rows[i].findAll('td')]
# for i in range(len(rows))]
# G_rows_data = G_rows_data[:10]
print(listting[:30])

#insert into table row by row General 
# cur.executemany("INSERT INTO GENERAL VALUES")





cur.close()
conn.close()

# #dataframe
# player_stats = pd.DataFrame(rows_data, columns=headers)

# #export to CSV
# player_stats.to_csv("players_stats.csv", index=False, sep=";")