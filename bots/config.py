import os
from dotenv import load_dotenv
import tweepy
import logging
load_dotenv()
logger = logging.getLogger()

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
        print("BIG ERROR")
        raise e
    logger.info("API created")
    print("API created")
    return api
create_api()