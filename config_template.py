import pymongo

"""
   Variables that contain user credentials for Twitter API as well as
   client for local MongoDB database.

    Intructions:

    - paste your own Twitter credentials into the empty strings.
    - when finished, save and rename this file as config.py (important!)
"""

### TWITTER CREDENTIALS ###
CONSUMER_API_KEY = ""
CONSUMER_API_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

### CONNECTING TO LOCAL MONGODB ###
LOCAL_CLIENT = pymongo.MongoClient()
