import os
from dotenv import load_dotenv
import tweepy 
import logging
import requests
import time
import sys
import inspect
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
# from tkinter.tix import INTEGER
load_dotenv()
logger = logging.getLogger()

## Creates API connection to twitter to make tweets
# You need to create your own twitter developer account to test out your twitter animations
# This function is only used in other files
def create_api():
    con_key = os.getenv("consumer_key")
    con_secret = os.getenv("consumer_secret")
    acc_token = os.getenv("access_token")
    acc_token_secret = os.getenv("access_token_secret")
    auth = tweepy.OAuthHandler(con_key, con_secret)
    auth.set_access_token(acc_token,acc_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

# Scrapes the entire page stats for every NBA player in given season
# returns headers and rows
#### TODO ####
# make the year modular, meaning when calling the function, you can change what year to scrape stats from
# Helper function for collect_data_season
def scrape_season_stats():
    #url I'm scraping
    url = "https://www.basketball-reference.com/leagues/NBA_2023_per_game.html"

    # collect html data
    #loops three times to make it stronger
    html = None   
    for i in [1,2,3]:        
        try:  
            r = requests.get(url, timeout=30)
            html = r.text
            if html: break
        except Exception as e:
            sys.stderr.write('Got error when requesting URL "' + url + '": ' + str(e) + '\n')
            if i == 3 :
                sys.stderr.write('{0.filename}@{0.lineno}: Failed requesting from URL "{1}" ==> {2}\n'.                       format(inspect.getframeinfo(inspect.currentframe()), url, e))
                raise e
            time.sleep(10*(i-1))
    # html = urlopen(url)

    #create beautiful soup object from HTML
    soup = BeautifulSoup(html, 'html.parser')

    # collect info from table header 
    headers = [th.getText() for th in soup.findAll('tr') 
    [0].findAll('th')]
    headers = headers[1:]
    #get rows from table
    rows = soup.findAll('tr', class_='full_table')
    ## The CSV file is to better visualize the data, it's commented out by default 
    # #dataframe
    # player_stats = pd.DataFrame(rows_data, columns=headers)
    # #export to CSV
    # player_stats.to_csv("players_stats.csv", index=False, sep=";")
    return headers, rows

# Iterates through each row and extracts text from all 'td' tags
# the 'td' tags in the website are where the stats are coming from
# Helper function for sort_categories
def collect_data_season(indices, list):
    headers, rows = scrape_season_stats()
    #Loops through each row 
    for i in range(len(rows)):
        # in each row, loop through headers and append the given indices
        for td in indices:
            list.append(rows[i].findAll('td')[td].getText())

# Formats a list by grouping into tuples to easily add onto tables
# Helper function for sort_categories
def convert(list, num):
    new_list = []
    for i in range(1, len(list)+1):
        if i % num == 0:
            new_list.append(tuple(list[i-num:i]))
    return new_list

# organizes data for database use
# helper function for db_season_stats
def sort_categories():
    headers, rows = scrape_season_stats()

    # when scraping data, each index represents a particular statistic
    # in these next few lines, we are grouping the statistics into different categories, the numbers representing different headers``
    # G == General, BOFF == Basic Offensive stats, AOFF == Advanced Offensive Stats, DEF == Defensive Stats
    Gindices = [0,1,2,3,4,5,6]
    BOFFindices = [7,8,10,11,13,14,17,18,23,28]
    AOFFindices = [9,12,15,16,19]
    DEFindices = [24,25]
    OTHERindices = [20,21,22,26,27]

    # picks the headers based off specified indices
    # Gheaders =  ['Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP']
    Gheaders = headers[:7]
    BOFFheaders = [headers[index] for index in BOFFindices]
    AOFFheaders = [headers[index] for index in AOFFindices]
    DEFheaders = [headers[index] for index in DEFindices]
    OTHERheaders = [headers[index] for index in OTHERindices]

    # initialize empty list for each statistical category
    Glist, BOFFlist, AOFFlist, DEFlist, OTHERlist = ([] for i in range(5))
    # Collecting and format data for table
    # The helper function uses the grouped indices (Gindices) to append to data into list (Glist)
    # Glist now contains all general stats from each player 
    # Glist = ['Precious Achiuwa', 'C', '22', 'TOR', '73', '28', '23.6', 'Steven Adams', 'C', '28', 'MEM', '76', '75', '26.3'...]
    collect_data_season(Gindices, Glist)
    collect_data_season(BOFFindices, BOFFlist)
    collect_data_season(AOFFindices, AOFFlist)
    collect_data_season(DEFindices, DEFlist)
    collect_data_season(OTHERindices, OTHERlist)

    # converts list into tuple groups per player
    # Glist = [('Precious Achiuwa', 'C', '22', 'TOR', '73', '28', '23.6'), ('Steven Adams', 'C', '28', 'MEM', '76', '75', '26.3')]
    Glist = convert(Glist, len(Gindices))
    BOFFlist = convert(BOFFlist, len(BOFFindices))
    AOFFlist = convert(AOFFlist, len(AOFFindices))
    DEFlist = convert(DEFlist, len(DEFindices))
    OTHERlist = convert(OTHERlist, len(OTHERindices))
    
    return Gheaders, BOFFheaders, AOFFheaders, DEFheaders, OTHERheaders, Glist, BOFFlist, AOFFlist, DEFlist, OTHERlist

# Creates database and tables and populates tables 
def db_season_stats():
    # call sort_categories for data
    Gheaders, BOFFheaders, AOFFheaders, DEFheaders, OTHERheaders, Glist, BOFFlist, AOFFlist, DEFlist, OTHERlist = sort_categories()
    # database connection
    conn = sqlite3.connect('my_database.db')
    cur = conn.cursor()

    ## INIT GENERAL Table
    # remove general table if it exists already
    cur.execute('DROP TABLE IF EXISTS GENERAL')
    # create table general with all general categories
    cur.execute('''CREATE TABLE GENERAL 
                (Player text, Pos text, Age INTEGER, Tm text, G INTEGER, GS INTEGER, MP real)''')
    # insert headers into table
    cur.execute('INSERT INTO GENERAL VALUES(?,?,?,?,?,?,?)', Gheaders)
    cur.execute('SELECT * FROM GENERAL')
    # print(f'this is general table: {cur.fetchall()}')

    ## INIT BOFF Table
    cur.execute('DROP TABLE IF EXISTS BOFF')
    cur.execute('''CREATE TABLE BOFF 
                (FG real, FGA real, THP real, THPA real, TWOP real, TWOPA real, FT real, FTA real, AST real, PTS real)''')
    cur.execute('INSERT INTO BOFF VALUES(?,?,?,?,?,?,?,?,?,?)', BOFFheaders)
    cur.execute('SELECT * FROM BOFF')
    # print(f'this is BOFF table: {cur.fetchall()}')

    ## INIT AOFF Table 
    cur.execute('DROP TABLE IF EXISTS AOFF')
    cur.execute('''CREATE TABLE AOFF 
                (FGP real, THPP real, TWOPP real, eFGP real, FTP real)''')
    cur.execute('INSERT INTO AOFF VALUES(?,?,?,?,?)', AOFFheaders)
    cur.execute('SELECT * FROM AOFF')
    # print(f'this is AOFF table: {cur.fetchall()}')

    ## INIT DEF Table 
    cur.execute('DROP TABLE IF EXISTS DEF')
    cur.execute('''CREATE TABLE DEF 
                (STL real, BLK real)''')
    cur.execute('INSERT INTO DEF VALUES(?,?)', DEFheaders)
    cur.execute('SELECT * FROM DEF')
    # print(f'this is DEF table: {cur.fetchall()}')

    ## INIT OTHER Table 
    cur.execute('DROP TABLE IF EXISTS OTHER')
    cur.execute('''CREATE TABLE OTHER 
                (ORB real, DRB real, TRB real, TOV real, PF real)''')
    cur.execute('INSERT INTO OTHER VALUES(?,?,?,?,?)', OTHERheaders)
    cur.execute('SELECT * FROM OTHER')
    # print(f'this is OTHER table: {cur.fetchall()}')

    # This commits all the added tables and categories, essential to keep it saved 
    conn.commit()

    # inserts values for all players for given categories 
    cur.executemany("INSERT INTO GENERAL VALUES(?,?,?,?,?,?,?)", (Glist))
    cur.executemany("INSERT INTO BOFF VALUES(?,?,?,?,?,?,?,?,?,?)", (BOFFlist))
    cur.executemany("INSERT INTO AOFF VALUES(?,?,?,?,?)", (AOFFlist))
    cur.executemany("INSERT INTO DEF VALUES(?,?)", (DEFlist))
    cur.executemany("INSERT INTO OTHER VALUES(?,?,?,?,?)", (OTHERlist))
    return conn, cur

# organize db data to make it tweet ready
#takes into account character limit, and makes separate tuples to tweet in a thread style
def tweet_ready_stats(players, player_stats):
    character_limit = 280
    reply = []
    for i in range(len(players)):
        # formulate reply for player and stat
        reply.append(f'''{i+1}. {players[i][1]} from {players[i][2]} {player_stats[i]}\n''')
    # groups thread into sections that will be just under the 280 character size limit
    num_list = []
    # an int value that keeps track of amount of times the reply has been changed 
    reply_changes = 0
    # new_reply will be where tuples are added onto
    new_reply = []
    for player in range(len(reply)):
        #take into account \n which adds a character
        character_limit -= 1
        print(f'character_limit: {character_limit}')
        #this gets reset when character limit is met
        num_list.append(player)
        print(f'this is num_list: {num_list}')
        if player == (len(reply)-1):
            break
        # if max character size is reached
        if sum(len(i) for i in reply[num_list[0]:(player+1)]) > character_limit:
            #resets character limit 
            character_limit = 280
            # create a tuple of max amount of players who will fit into one tweet
            # append tuple to new reply
            new_reply.append(tuple(reply[ num_list[0] : player ]))
            # clear list so next first index of new_list matches the tuple creation's beginning index
            reply_changes += 1
            num_list.clear()
            num_list.append(player)
    # extend based on all numbers outside the tuple
    # without using reply[1] because it may not even be the second index
    new_reply.append(tuple(reply[num_list[0]:]))
    reply = new_reply
    logger.info(f"This is the tweet with the total number of replies:\n{reply}\n{len(reply)}")
    print(4)
    reply = [" ".join(tuples) for tuples in reply]
    print(reply)
    return reply

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

# Converts decimal values to percent values
def convert_decimal_to_percent(list1):
    new_list = []
    for val in list1:
        new_list.append(str(round(val*100)) + '%')
    print(f'this is the new_list: {new_list}')
    return new_list