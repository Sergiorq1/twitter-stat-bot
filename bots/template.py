# This is the bot template, copy this whenever new bto is made 
# from config file
from config import db_season_stats, create_api, tweet_ready_stats, sort_tuples, convert_decimal_to_percent

# for bot files
from datetime import date
import logging
import tweepy
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

### TODO: Change function to retrieve necessary data from database ###
def get_db_stats():
    conn, cur = db_season_stats()
    ### TODO: Select what data to pull from ###
    cur.execute('''SELECT *
                   FROM GENERAL''')
    stats = cur.fetchall()
    conn.commit()
    # SELECT FROM GENERAL table to get names of NBA players using tuple numbers
    # ordered list of highest to lowest efg%
    player_id = list(i[0] for i in stats)
    player_stats = list(i[1] for i in stats)
    efgp_players = 'SELECT rowid, Player, TM FROM GENERAL where rowid IN ({seq})'.format(
        seq=','.join(['?']*len(player_id)))
    cur.execute(efgp_players, player_id)
    players = cur.fetchall()
    sorted_players = sort_tuples(player_id, players)
    cur.close()
    conn.close()
    return sorted_players, player_stats

# executes tweet with replies 
### TODO: Change function to include new  ###
def top_efgp_tweet():
    api = create_api()
    players = get_db_stats()[0]
    player_stats = get_db_stats()[1]
    player_stats = convert_decimal_to_percent(player_stats)
    reply = tweet_ready_stats(players, player_stats)
    #tweets out the grouped sections 
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    logger.info("Tweeting top 20 ***Insert bot functionality here***")
    # Initialize Tweet to build thread under
    tweet = f"Top 20 ***Insert bot functionality here*** (as of {d1}), a thread \U0001F9F5:"
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