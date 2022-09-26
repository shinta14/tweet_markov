import tweepy
from pprint import pprint
import schedule
from time import sleep
import markov_chain
import random

def ClientInfo():
    client = tweepy.Client(bearer_token    = BEARER_TOKEN,
                           consumer_key    = API_KEY,
                           consumer_secret = API_SECRET,
                           access_token    = ACCESS_TOKEN,
                           access_token_secret = ACCESS_TOKEN_SECRET,
                          )
    
    return client

message = markov_chain.sentence


def CreateTweet(message):
    tweet = ClientInfo().create_tweet(text=message)
    return tweet




def SendMessage():
    pprint(CreateTweet(message))

schedule.every(10).seconds.do(SendMessage)

while True:
    schedule.run_pending()
    sleep(1)