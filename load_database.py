'''
The purpose of this script is to build upon the twitter_streamer.py script --
by importing its TwitterStreamer class and loading the collected, streamed tweets
into a MongoDB database.
'''

import argparse

import config
from twitter_streamer import TwitterStreamer

LOCAL_DB = config.LOCAL_CLIENT.twitter_data
#create a Mongo database called twitter_data

class LoadDatabase():

    def __init__(self, batch_size, limit):
        self.batch_size = batch_size
        self.buffer = []
        self.limit = limit
        self.counter = 0

    def load_tweets(self, tweet):
        '''
            The primary method to be used as the callback function on each
            incoming tweet. Each tweet is appended to an empty list (the "buffer")
            and as soon as this buffer is full (i.e. has reached the batch size),
            the tweets are dumped into Mongo DB.
        '''
        self.buffer.append(tweet)

        #logic for handling if batch size > limit and if limit % batch_size != 0
        if self.limit - self.counter < self.batch_size:
            self.batch_size = self.limit - self.counter

        #main block
        if len(self.buffer) >= self.batch_size:
            LOCAL_DB.tweet_dicts.insert_many(self.buffer)
            print(f"loaded {int(self.counter + self.batch_size)} tweets of\
            {int(self.limit)}\n")
            self.buffer = []
            self.counter += self.batch_size

def populate_database(batch_size, limit, keywords):

    '''The primary function of this script. Instantiates the TwitterStreamer
       class imported from the twitter_streamer.py script, and replaces the
       default callback function (print) with the load_tweets method defined
       in the LoadDatabase() class above.
    '''

    callback_function = LoadDatabase(batch_size, limit).load_tweets

    twitter_streamer = TwitterStreamer(keywords)
    twitter_streamer.stream_tweets(limit, callback_function)


if __name__ == '__main__':

    """
    To view argument parser help in the command line:
    'python load_database.py -h'
    """

    parser = argparse.ArgumentParser(description='Collect tweets and put them\
    into a database.')

    parser.add_argument('-k', '--keyword_list',
                        nargs='+',
                        help='<Required> Enter any keywords (separated by spaces;\
                        no punctuation) that should be included in streamed tweets.',
                        required=True)

    parser.add_argument('-b', '--batch_size',
                        type=int,
                        default=2,
                        help='How many tweets do you want to grab at a time?')

    parser.add_argument('-n', '--total_number',
                        type=int,
                        default=10,
                        help='How many total tweets do you want to get?')

    args = parser.parse_args()

    print(f"\nLoading tweets about {args.keyword_list} into database...\
          \nWait for progress status...\n\n")
    populate_database(args.batch_size, args.total_number, args.keyword_list)
