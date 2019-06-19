"""
The purpose of this script is to intercept real-time, streamed tweets
using some of tweepy's built-in Classes:

    1. OAuthHandler
        - for authenticating API keys, tokens, etc.

    2. StreamListener
        - to use as a template for creating a custom
          TwitterListener class, which decides how to parse each
          tweet (JSON string) as it is intercepted.

    3. Stream
        - acts as a container for the OAuthHAndler and the StreamListener.
        - can be used to filter incoming tweets by keywords and language.

After each relevant, incoming tweet is intercepted and parsed, it is printed
in the terminal (print is the default callback function). The keyword can be
altered at the end of the script.

"""

import json
from datetime import datetime # solely for testing script execution time.

from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

import config

STARTTIME = datetime.now()
LANGUAGES = ['en']

def get_geo_data(tweet):

    geo_data = []
    if tweet['place'] != None:
        try:
            geo_data.append(tweet['place']['full_name'])
            geo_data.append(tweet['place']['bounding_box']['coordinates'])
        except KeyError:
            geo_data.append(['KeyError'])

    return geo_data

def get_user_location(tweet):

    '''Function that extracts location of the user / author of each tweet,
       which comes in as a JSON string.
    '''

    user_location = []
    if tweet['user']['location'] != None:
        try:
            user_location.append(tweet['user']['location'])
        except KeyError:
            user_location.append(['KeyError'])

    return user_location

def get_hashtags(tweet):

    '''Function that extracts the hashtags from each tweet,
       which comes in as a JSON string.
    '''

    hashtags = []
    if 'extended_tweet' in tweet:
        for hashtag in tweet['extended_tweet']['entities']['hashtags']:
            hashtags.append(hashtag['text'])
    elif 'hashtags' in tweet['entities'] and len(tweet['entities']['hashtags']) > 0:
        hashtags = [item['text'] for item in tweet['entities']['hashtags']]

    return hashtags

def get_tweet_dict(tweet):

    '''Function that extracts relevant information from the tweet
       (using the 3 user-defined functions from above) and structures the
       data into a dictionary -- in preparation for loading into MongoDB.
    '''

    if 'extended_tweet' in tweet:
        text = tweet['extended_tweet']['full_text']
    else:
        text = tweet['text']

    geo_data = get_geo_data(tweet)
    user_location = get_user_location(tweet)
    hashtags = get_hashtags(tweet)

    tweet = {'id': tweet['id_str'],
             'tweet_created_at': tweet['created_at'],
             'text': text,
             'user': tweet['user']['screen_name'],
             'source': tweet['source'],
             'language': tweet['lang'],
             'user_description': tweet['user']['description'],
             'num_followers':tweet['user']['followers_count'],
             'user_statuses': tweet['user']['statuses_count'],
             'user_created_at': tweet['user']['created_at'],
             'hashtags': hashtags,
             'tweet_location': geo_data,
             'user_location': user_location,
             }
    return tweet

class TwitterAuthenticator():

    """Class, whose sole purpose is to provide authentication to use
       the Twitter API.
    """
    def authenticate(self):
        """
        Use tweepy's built-in OAuthHandler class to return authentication object.
        """
        auth = OAuthHandler(config.CONSUMER_API_KEY, config.CONSUMER_API_SECRET)
        auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
        return auth

class TwitterListener(StreamListener):

    '''Required Class that inherits from tweepy.StreamListener.
       The 'on_data()' method dictates what should be done with tweets
       as soon as they come in contact with the Listener / program.
    '''

    def __init__(self, limit, callback):
        super().__init__() # Inherit __init__ method from parent class.
        self.limit = limit
        self.counter = 0
        self.callback = callback

    def on_error(self, status):

        '''DEFAULT method inherited from StreamListener class.

           Kills the connection if rate-limiting occurs.
           see: https://developer.twitter.com/en/docs/basics/response-codes
        '''

        if status == 420:
            return 420
        print(status)

    def on_data(self, data):

        '''DEFAULT method inherited from StreamListener class.

           This is the main function of the Twitter Streamer class.

           It defines what should be done with each incoming streamed tweet as it
           is intercepted by the StreamListener:

           - convert each json-like string from twitter into a workable JSON object;
           - ignore retweets, replies, and quoted tweets;
           - apply the get_tweet_dict function to each object;
           - apply a callback function to the resulting dictionary;
           - shut off StreamListener as soon as it reaches a pre-defined limit.
        '''

        t = json.loads(data)

        is_tweet_reply = t['in_reply_to_status_id'] == None
        is_quote = t['is_quote_status'] == False

        if 'RT' not in t['text'] and is_tweet_reply and is_quote:

            tweet = get_tweet_dict(t)
            self.callback(tweet)

            self.counter += 1

            if self.counter == self.limit:
                return False

class TwitterStreamer():
    '''
       Class containing the primary method / functionality of the script.
    '''

    def __init__(self, keywords):
        self.twitter_authenticator = TwitterAuthenticator()
        self.keywords = keywords

    def stream_tweets(self, limit, callback):
        '''
            Primary function that wraps up all preceeding code into one method.
        '''
        listener = TwitterListener(limit, callback)
        auth = self.twitter_authenticator.authenticate()
        stream = Stream(auth, listener)
        stream.filter(track=self.keywords, languages=LANGUAGES)


if __name__ == "__main__":

    twitter_streamer = TwitterStreamer(['berlin'])
    twitter_streamer.stream_tweets(10, print)
