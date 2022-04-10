import tweepy
import logging
from config import create_api
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def good_morning(api):
    logger.info("Sending good morning message")
    message = "Hello world!"
    api.update_status(message)

def main():
    api = create_api()
    while True:
        good_morning(api)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()