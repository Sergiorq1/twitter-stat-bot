import os
from dotenv import load_dotenv
import tweepy 
import logging
import requests
import time
import sys
import inspect
# from tkinter.tix import INTEGER
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
load_dotenv()
logger = logging.getLogger()

# Creates API connection to twitter to make tweets
## You need to create your own twitter developer account to test out your twitter animations
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
def scrape_season_stats():
    #url I'm scraping
    url = "https://www.basketball-reference.com/leagues/NBA_2022_per_game.html"

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
    # #dataframe
    # player_stats = pd.DataFrame(rows_data, columns=headers)
    # #export to CSV
    # player_stats.to_csv("players_stats.csv", index=False, sep=";")
    return headers, rows

# Iterates through each row and extracts text from all 'td' tags
def collect_data_season(indices, list):
    headers, rows = scrape_season_stats()
    for i in range(len(rows)):
        for td in indices:
            list.append(rows[i].findAll('td')[td].getText())
# Formats a list by grouping into tuples to easily add onto tables
def convert(list, num):
    new_list = []
    for i in range(1, len(list)+1):
        if i % num == 0:
            new_list.append(tuple(list[i-num:i]))
    return new_list
# Creates database and tables and populate tables 
def db_season_stats():
    headers, rows = scrape_season_stats()
    # database connection
    conn = sqlite3.connect('my_database.db')
    cur = conn.cursor()
    
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
    Gheaders = headers[:7]
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
    conn.commit()
    #collecting and format data for table
    collect_data_season(Gindices, Glist)
    collect_data_season(BOFFindices, BOFFlist)
    collect_data_season(AOFFindices, AOFFlist)
    collect_data_season(DEFindices, DEFlist)
    collect_data_season(OTHERindices, OTHERlist)
    Glist = convert(Glist, len(Gindices))
    BOFFlist = convert(BOFFlist, len(BOFFindices))
    AOFFlist = convert(AOFFlist, len(AOFFindices))
    DEFlist = convert(DEFlist, len(DEFindices))
    OTHERlist = convert(OTHERlist, len(OTHERindices))

    cur.executemany("INSERT INTO GENERAL VALUES(?,?,?,?,?,?,?)", (Glist))
    cur.executemany("INSERT INTO BOFF VALUES(?,?,?,?,?,?,?,?,?,?)", (BOFFlist))
    cur.executemany("INSERT INTO AOFF VALUES(?,?,?,?,?)", (AOFFlist))
    cur.executemany("INSERT INTO DEF VALUES(?,?)", (DEFlist))
    cur.executemany("INSERT INTO OTHER VALUES(?,?,?,?,?)", (OTHERlist))
    return conn, cur


            


