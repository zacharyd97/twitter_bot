import tweepy
from dotenv import load_dotenv
import os
import random
import logging
import time

load_dotenv()

# Load API keys and tokens
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")

# Authenticate
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Initialize logging
logging.basicConfig(filename='twitter_bot.log', level=logging.INFO)


def tweet_random_tweet():
    try:
        with open("tweets.txt", "r", encoding="utf-8") as file:
            tweets = file.read().splitlines()

        random_tweet = random.choice(tweets)

        # Create a new tweet
        api.update_status(random_tweet)
        logging.info("Tweeted: %s", random_tweet)
    except Exception as error:
        logging.error("Error tweeting: %s", error)


def respond_to_mentions():
    message = 'Hello, I am an automated bot. You can contact my creator at zdowell97@gmail.com or via direct message.'
    try:
        # Fetch mentions
        mentions = api.mentions_timeline(since_id=get_last_mention_id(), tweet_mode='extended')
        
        # Respond to mentions
        for mention in reversed(mentions):  # Process mentions in reverse chronological order
            tweet_id = mention.id
            tweet_user = mention.user.screen_name
            api.update_status(f"@{tweet_user} {message}", in_reply_to_status_id=tweet_id)
            logging.info("Replied to mention: %s", tweet_id)

        update_last_mention_id()  # Update the last mention ID
    except Exception as error:
        logging.error("Error responding to mentions: %s", error)


def get_last_mention_id():
    # Retrieve the last mention ID from a file or database
    try:
        with open("last_mention_id.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 1  # Start from the beginning if the file doesn't exist


def update_last_mention_id():
    # Update the last mention ID in a file or database
    try:
        with open("last_mention_id.txt", "w") as file:
            file.write(str(api.mentions_timeline(count=1)[0].id))
    except Exception as error:
        logging.error("Error updating last mention ID: %s", error)


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
