import tweepy
from dotenv import load_dotenv
import os
import random
import logging
import schedule
import time

# Load API keys and tokens
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Authenticate with OAuth 2.0 User Context
auth = tweepy.Client(BEARER_TOKEN)

# Initialize Tweepy API
api = tweepy.Client(auth, API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Initialize logging
logging.basicConfig(filename='twitter_bot.log', level=logging.INFO)

def tweet_random_tweet():
    try:
        with open("tweets.txt", "r", encoding="utf-8") as file:
            tweets = file.read().splitlines()
        
        random_tweet = random.choice(tweets)

        # Create a new tweet
        api.create_tweet(text=random_tweet)
        
        logging.info("Tweeted: %s", random_tweet)
    except Exception as error:
        logging.error("Error tweeting: %s", error)

def main():
    # Schedule the tweet to run daily at 9:00 AM
    schedule.every().day.at('09:00').do(tweet_random_tweet)

    # Continuous execution of scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()