import tweepy
from dotenv import load_dotenv
import os
import time
import schedule
import random
import logging

load_dotenv()
    
# Load API keys and tokens
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")

client = tweepy.Client(BEARER_TOKEN,API_KEY,API_KEY_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
api = tweepy.API(auth)


# Initialize logging
logging.basicConfig(filename='twitter_bot.log', level=logging.INFO)

def tweet_random_tweet():
    try:
        with open("tweets.txt", "r", encoding="utf-8") as file:
            tweets = file.read().splitlines()
        
        random_tweet = random.choice(tweets)
        
        
        # Create a new tweet
        client.create_tweet(text=random_tweet)
        
        logging.info("Tweeted: %s", random_tweet)
    except Exception as error:
        logging.error("Error tweeting: %s", error)


def respond_to_mentions():
    message = 'Hello i am an automated bot, you can contact my creator at zdowell97@gmail.com or with direct message'
    try:
        client_id = client.get_me().data.id
        start_id = 1
        initialization_resp = client.get_user_mentions(client_id)
        if initialization_resp.data is not None:
            start_id = initialization_resp.data[0].id
        

        while True:
            response = client.get_user_mentions(client_id, since_id=start_id)
            if response.data is not None:
                for tweet in response.data:
                    try:
                        print(tweet.text)
                        client.create_tweet(in_reply_to_tweet_id=tweet.id, text=message)
                        start_id = tweet.id
                    except Exception as error:
                        logging.error("Error responding to mention: %s", error)
            time.sleep(30)
    except Exception as error:
        logging.error("Error in respond_to_mentions: %s", error)

def main():

    # Schedule the tweet to run daily at 9:00 AM
    schedule.every().day.at('09:00').do(tweet_random_tweet)
    
    # Schedule the mention response to run continuously
    schedule.every(1).minutes.do(respond_to_mentions)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Bot stopped by user")
            break



if __name__ == "__main__":
    main()



