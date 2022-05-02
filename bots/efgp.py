# 10 highest ppg of current season
from tkinter.tix import INTEGER
from urllib.request import urlopen
from bs4 import BeautifulSoup
from config import scrape_season_stats, collect_data_season, convert, db_season_stats
import pandas as pd
import sqlite3

scrape_season_stats()
collect_data_season()
db_season_stats()
##### GET top 10 players with highest effective FG percentage #####
def top_efgp():
    conn, cur = db_season_stats()
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
    cur.close()
    conn.close()
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


