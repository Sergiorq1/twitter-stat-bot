### Effective field goal percentage leaders in a season ###
#from config file
from config import db_season_stats, create_api, tweet_ready_stats

#for bot files
from datetime import date
import logging
import tweepy
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# gets top 10 players with highest effective FG percentage
def top_efgp():
    conn, cur = db_season_stats()
    # find 10 highest numbers in eFG%
    # sort from Greatest to lowest, and also retrieve tuple numbers that correspond
    cur.execute('SELECT rowid, EFGP FROM AOFF GROUP BY EFGP HAVING EFGP < 1.1 ORDER BY EFGP DESC LIMIT 20')
    EFGP_stats = cur.fetchall()
    # print(f'these are the top 10 players with the highest Effective field goal percentage: {EFGP_stats}')
    conn.commit()
    # SELECT FROM GENERAL table to get names of NBA players using tuple numbers
    # ordered list of highest to lowest efg%
    player_id = list(i[0] for i in EFGP_stats)
    player_stats = list(i[1] for i in EFGP_stats)
    efgp_players = 'SELECT rowid, Player, TM FROM GENERAL where rowid IN ({seq})'.format(
        seq=','.join(['?']*len(player_id)))
    cur.execute(efgp_players, player_id)
    players = cur.fetchall()
    cur.close()
    conn.close()
    return players, player_stats

# executes tweet with replies 
def top_efgp_tweet():
    api = create_api()
    players = top_efgp()[0]
    player_stats = top_efgp()[1]
    reply = tweet_ready_stats(players, player_stats)
    #tweets out the grouped sections 
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    logger.info("Tweeting top 20 effective field goal percentage havers")
    # Initialize Tweet to build thread under
    tweet = f"Top 20 NBA EFG% players (as of {d1}), a thread \U0001F9F5:"
    tweet_head = api.update_status(status=tweet)

    for i in range(len(reply)):
        if i == 0:
            #This makes sure to reply to tweet head
            thread_init = api.update_status(status=reply[i],in_reply_to_status_id=tweet_head.id,auto_populate_reply_metadata=True)
        elif i == 1:
            #This makes sure to reply to first reply
            after = api.update_status(status=reply[i],in_reply_to_status_id=thread_init.id,auto_populate_reply_metadata=True)  
        else:
            #This makes sure to reply to latest reply from thread
            after = api.update_status(status=reply[i],in_reply_to_status_id=after.id,auto_populate_reply_metadata=True) 
    return "Tweet has been Tweeted!"

print(top_efgp_tweet())
        
