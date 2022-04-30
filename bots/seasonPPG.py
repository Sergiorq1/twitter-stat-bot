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
Glist = []
BOFFlist = []
AOFFlist = []
DEFlist = []
OTHERlist = []
BOFFheaders = [headers[index] for index in BOFFindices]
AOFFheaders = [headers[index] for index in AOFFindices]
DEFheaders = [headers[index] for index in DEFindices]
OTHERheaders = [headers[index] for index in OTHERindices]

#  INIT GENERAL Table
cur.execute('DROP TABLE IF EXISTS GENERAL')
cur.execute('''CREATE TABLE GENERAL 
            (Player text, Pos text, Age INTEGER, Tm text, G INTEGER, GS INTEGER, MP real)''')
cur.execute('INSERT INTO GENERAL VALUES(?,?,?,?,?,?,?)', Gheaders)
cur.execute('SELECT * FROM GENERAL')
print(f'this is general table: {cur.fetchall()}')

# INIT BOFF Table
cur.execute('DROP TABLE IF EXISTS BOFF')
cur.execute('''CREATE TABLE BOFF 
            (FG real, FGA real, THP real, THPA real, TWOP real, TWOPA real, FT real, FTA real, AST real, PTS real)''')
cur.execute('INSERT INTO BOFF VALUES(?,?,?,?,?,?,?,?,?,?)', BOFFheaders)
cur.execute('SELECT * FROM BOFF')
print(f'this is BOFF table: {cur.fetchall()}')

# INIT AOFF Table 
cur.execute('DROP TABLE IF EXISTS AOFF')
cur.execute('''CREATE TABLE AOFF 
            (FGP real, THPP real, TWOPP real, eFGP real, FTP real)''')
cur.execute('INSERT INTO AOFF VALUES(?,?,?,?,?)', AOFFheaders)
cur.execute('SELECT * FROM AOFF')
print(f'this is AOFF table: {cur.fetchall()}')

# INIT DEF Table 
cur.execute('DROP TABLE IF EXISTS DEF')
cur.execute('''CREATE TABLE DEF 
            (STL real, BLK real)''')
cur.execute('INSERT INTO DEF VALUES(?,?)', DEFheaders)
cur.execute('SELECT * FROM DEF')
print(f'this is DEF table: {cur.fetchall()}')

# INIT OTHER Table 
cur.execute('DROP TABLE IF EXISTS OTHER')
cur.execute('''CREATE TABLE OTHER 
            (ORB real, DRB real, TRB real, TOV real, PF real)''')
cur.execute('INSERT INTO OTHER VALUES(?,?,?,?,?)', OTHERheaders)
cur.execute('SELECT * FROM OTHER')
print(f'this is OTHER table: {cur.fetchall()}')
#Convert function to create tuples
def convert(list, num):
    new_list = []
    for i in range(1, len(list)+1):
        if i % num == 0:
            new_list.append(tuple(list[i-num:i]))
    return new_list
#get rows from table
rows = soup.findAll('tr', class_='full_table')

#collecting and format data for table
 
def collectData(indices, list):
    for i in range(len(rows)):
        for td in indices:
            list.append(rows[i].findAll('td')[td].getText())
collectData(Gindices, Glist)
collectData(BOFFindices, BOFFlist)
collectData(AOFFindices, AOFFlist)
collectData(DEFindices, DEFlist)
collectData(OTHERindices, OTHERlist)
Glist = convert(Glist, len(Gindices))
BOFFlist = convert(BOFFlist, len(BOFFindices))
AOFFlist = convert(AOFFlist, len(AOFFindices))
DEFlist = convert(DEFlist, len(DEFindices))
OTHERlist = convert(OTHERlist, len(OTHERindices))

cur.executemany("INSERT INTO GENERAL VALUES(?,?,?,?,?,?,?)", (Glist))
cur.executemany("INSERT INTO BOFF VALUES(?,?,?,?,?,?,?,?,?,?)", (BOFFlist))
cur.executemany("INSERT INTO AOFF VALUES(?,?,?,?,?)", (AOFFlist))

##### GET top 10 players with highest effective FG percentage #####
# find 10 highest numbers in eFG%
# sort from Greatest to lowest, and also retrieve tuple numbers that correspond
cur.execute('SELECT rowid, EFGP FROM AOFF GROUP BY EFGP HAVING EFGP < 1.1 ORDER BY EFGP DESC LIMIT 20')
EFGP_stats = cur.fetchall()
# print(f'these are the top 10 players with the highest Effective field goal percentage: {EFGP_stats}')
conn.commit()
# SELECT FROM GENERAL table to get names of NBA players using tuple numbers
#ordered list of highest to lowest efg%
player_id = list(i[0] for i in EFGP_stats)
efgp_players = 'SELECT rowid, Player, TM FROM GENERAL where rowid IN ({seq})'.format(
    seq=','.join(['?']*len(player_id)))
cur.execute(efgp_players, player_id)
players = cur.fetchall()
# reorganize players list by comaring it to player_id
def sort_this(sorted_list,tuple_list):
    #only loops once
    for id in range(len(sorted_list)):
        #loops as many times as necessary
        for i in range(len(tuple_list)):
            # if current index value num matches current index 
            if tuple_list[i][0] == sorted_list[id]:
                tuple_list.insert(id, tuple_list[i])
                #if tuple_list index position is greater than index position of s_list
                if i > id:
                    tuple_list.pop(i+1)
                else:
                    tuple_list.pop(i)
                break
            else:
                continue

    return tuple_list
print(sort_this(player_id, players))
print(player_id)



                    


# make a twitter post that uses acquired data to automate EFG% 




cur.close()
conn.close()

# #dataframe
# player_stats = pd.DataFrame(rows_data, columns=headers)

# #export to CSV
# player_stats.to_csv("players_stats.csv", index=False, sep=";")