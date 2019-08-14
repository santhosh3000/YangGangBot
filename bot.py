################################################################
# Twitter: @YangGangBot
# Made by: Santhosh Abraham
################################################################
# Libraries
import tweepy
import time

from keys import *
from hashtags import *

################################################################
# Twitter's API Keys. Keys' ID stored in 'keys.py'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
################################################################
# File stores tweets' id that the bot already replied to.
# This avoids replying to the same tweet multiple times
FILE_NAME = 'last_seen_id.txt'


def read_last_seen_id(file_name):
    f = open(file_name, 'r')
    last_seen_id = int(f.read().strip())
    f.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f = open(file_name, 'w')
    f.write(str(last_seen_id))
    f.close()
    return
################################################################


def reply_to_tweets():
    print('looking for tweets...')
    last_seen_id = read_last_seen_id(FILE_NAME)

    mentions = api.mentions_timeline(
        last_seen_id,
        tweet_mode='extended')

    for mention in reversed(mentions):
        print(f'{str(mention.id)} - {mention.full_text}')
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)

        for key, value in hashtags.items():
            if key in mention.full_text.lower():
                print("Found", key)
                print('responding back...')
                api.update_status('@' +
                                  mention.user.screen_name +
                                  " " +
                                  str(value['response']),
                                  mention.id)


while True:
    reply_to_tweets()
    time.sleep(10)
