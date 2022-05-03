# 10 highest ppg of current season
from tkinter.tix import INTEGER
from urllib.request import urlopen
from bs4 import BeautifulSoup
from config import scrape_season_stats, collect_data_season, convert, db_season_stats
import pandas as pd
import sqlite3
import tweepy
import logging
from config import create_api
import time

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
    return player_id, players

# reorganize players list by comaring it to a given list, only works correctly if match
def sort_tuples(sorted_list,tuple_list):
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

#Calling functions
scrape_season_stats()
db_season_stats()
top_efgp()
player_id, players = top_efgp()
print(sort_tuples(player_id, players))
print(player_id)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def top_efgp_tweet(api):
    logger.info("Tweeting top 20 effective field goal percentage havers")
    #Initialize Tweet to make thread after
    message = "Top 20 NBA EFG%% players, a thread:"
    

    api.update_status(message)

def main():
    api = create_api()
    while True:
        top_efgp_tweet(api)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
# make a twitter post that uses acquired data to automate EFG% 


