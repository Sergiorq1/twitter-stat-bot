### Effective field goal percentage leaders in a season ###
#from config file
from config import db_season_stats, create_api

#for bot files
from datetime import date
import logging
import tweepy
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

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
    # ordered list of highest to lowest efg%
    player_id = list(i[0] for i in EFGP_stats)
    player_stats = list(i[1] for i in EFGP_stats)
    efgp_players = 'SELECT rowid, Player, TM FROM GENERAL where rowid IN ({seq})'.format(
        seq=','.join(['?']*len(player_id)))
    cur.execute(efgp_players, player_id)
    players = cur.fetchall()
    cur.close()
    conn.close()
    return player_id, players, player_stats

# reorganize players list by comparing it to a given list, only works correctly if match
def sort_tuples(sorted_list,tuple_list):
    # only loops once
    for id in range(len(sorted_list)):
        # loops as many times as necessary
        for i in range(len(tuple_list)):
            # if current index value num matches current index 
            if tuple_list[i][0] == sorted_list[id]:
                tuple_list.insert(id, tuple_list[i])
                # if tuple_list index position is greater than index position of s_list
                if i > id:
                    tuple_list.pop(i+1)
                else:
                    tuple_list.pop(i)
                break
            else:
                continue
    return tuple_list

# Calling functions from config.py
db_season_stats()
top_efgp()
player_id, players = top_efgp()[:2]

def top_efgp_tweet():
    api = create_api()
    player_stats = top_efgp()[2]

    reply = []
    for i in range(len(players)):
        # formulate reply player from team percentage
        reply.append(f'''{players[i][1]} from {players[i][2]} ({player_stats[i]})''')
    # print(reply)
    # groups thread into sections that will be just under the 280 character size limit
    num_list = []
    reply_changes = []
    for player in range(len(reply)):
        num_list.append(player)
        # if max character size is reached
        if sum(len(i) for i in reply[num_list[0]:(player)]) > 280:
            # create a tuple of max amount of players who will fit into one tweet
            # first add tuple in front of soon-to-be-removed indices
            reply.insert(player+1, tuple(reply[ num_list[0] : (num_list[0]+(len(num_list)-2)) ]))
            # remove duplicated
            reply = reply[:(player+1)-len(num_list)] + reply[player+1:]
            # clear list so next first index of new_list matches the tuple creation's beginning index
            reply_changes.append(1)
            num_list.clear()
    # extend based on all numbers outside the tuple
    # without using reply[1] because it may not even be the second index
    insert_len = len(reply[len(reply_changes):])
    reply.insert(-1, tuple(reply[len(reply_changes):]))
    reply.pop()
    reply = reply[:len(reply_changes)] + reply[insert_len:]
    # print(f"This should be it..... {reply}")
    # print(reply, len(reply))
    # print(f'this is sum of first tuple reply {sum(len(i) for i in reply[0])}')
    # print(f'this is sum of SECOND tuple reply {sum(len(i) for i in reply[1])}')
    #tweets out the grouped sections 
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    logger.info("Tweeting top 20 effective field goal percentage havers")
    # Initialize Tweet to build thread under
    tweet = f"Top 20 NBA EFG% players (as of {d1}), a thread \U0001F9F5:"
    tweet_head = api.update_status(status=tweet)
    # print(f'this is too large {reply[0]}')
    #reformats tuples into tweet form
    # for tuple in range(len(tweet)):
    #     " \n".join(tuple)

    reply = [" ".join(tups) for tups in reply]
    for i in range(len(reply)):
        if i == 0:
            thread_init = api.update_status(status=reply[i],in_reply_to_status_id=tweet_head.id,auto_populate_reply_metadata=True)
        elif i == 1:
            after = api.update_status(status=reply[i],in_reply_to_status_id=thread_init.id,auto_populate_reply_metadata=True)  
        else:
            after = api.update_status(status=reply[i],in_reply_to_status_id=after.id,auto_populate_reply_metadata=True)  


print(top_efgp_tweet())
        
