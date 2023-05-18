### Effective field goal percentage leaders in a season, with 6.5 field goal attempts per game or higher ###
# from config file
from config import db_season_stats, create_api, tweet_ready_stats, sort_tuples

# for bot files
from datetime import date
import logging
import tweepy
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# gets top 20 volume scoring players with highest effective field goal percentage
def top_volume_efgp():
    conn, cur = db_season_stats()
    # find 10 highest numbers in eFG% for volume scorers
    # sort from Greatest to lowest, and also retrieve tuple numbers that correspond
    cur.execute('''SELECT t1.rowid, t1.EFGP 
                   FROM AOFF AS t1
                   INNER JOIN BOFF AS t2 
                   ON t1.rowid = t2.rowid
                   WHERE t2.FGA >= 6.5 AND t1.rowid > 1
                   GROUP BY t1.EFGP 
                   ORDER BY t1.EFGP 
                   DESC LIMIT 20
                ''')
    EFGP_stats = cur.fetchall()
    # print(f'these are the top 10 volume scorers with the highest Effective field goal percentage: {EFGP_stats}')
    conn.commit()
    # SELECT FROM GENERAL table to get names of NBA players using tuple numbers
    # ordered list of highest to lowest efg%
    player_id = list(i[0] for i in EFGP_stats)
    player_stats = list(i[1] for i in EFGP_stats)
    efgp_players = '''SELECT rowid, Player, TM 
                      FROM GENERAL 
                      WHERE rowid IN ({seq})'''.format(seq=','.join(['?']*len(player_id)))
    cur.execute(efgp_players, player_id)
    players = cur.fetchall()
    # efgp_players removes the order in which the players are, so we need to re-sort it relative to player_id
    sorted_players = sort_tuples(player_id, players)
    # print(f'these are the sorted players: {sorted_players}')
    # print(f"these are the player's stats {player_stats}")
    cur.close()
    conn.close()
    return sorted_players, player_stats

def convert_decimal_to_percent(list1):
    new_list = []
    for val in list1:
        new_list.append(str(round(val*100)) + '%')
    print(f'this is the new_list: {new_list}')
    return new_list
# executes tweet with replies 
def top_volume_efgp_tweet():
    api = create_api()
    players = top_volume_efgp()[0]
    player_stats = top_volume_efgp()[1]
    player_stats = convert_decimal_to_percent(player_stats)
    reply = tweet_ready_stats(players, player_stats)
    #tweets out the grouped sections 
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    logger.info("Tweeting top 20 volume effective field goal percentage havers")
    # Initialize Tweet to build thread under
    tweet = f"Top 20 efg% players in the NBA with 6.5 field goal attempts or more. (as of {d1}), a thread \U0001F9F5:"
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

print(top_volume_efgp_tweet())
