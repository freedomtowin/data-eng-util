import pandas as pd
import os 
import json
import time

creds = json.load(open('security/twitter_cred.json','r'))
                  

consumer_key = creds['consumer_key']
consumer_secret = creds['consumer_secret']
access_token = creds['access_token']
access_token_secret = creds['access_token_secret']

import tweepy

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


db_fpath='data/chipmaker_tweet_archive_{}.csv'.format(int(time.time()))

if ~os.path.exists(db_fpath):
    handle = open(db_fpath,'w')
    handle.close()
    
makers=['nvidia','XilinxInc','AMD','latticesemi','intel']
sym = ['NVDA','XLNX','AMD','LSCC','INTC']

tweet_df = pd.DataFrame(columns=('time','tweet','maker'))

for i in range(len(makers)):
    maker = makers[i]
    query = 'from:'+maker
    max_tweets = 1000
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=query, tweet_mode='extended').items(max_tweets)]

    import datetime
    import subprocess
    import pandas as pd

    import time

    def datetime_from_utc_to_local(utc_datetime):
        now_timestamp = time.time()
        offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
        return utc_datetime + offset

    def datetime_from_local_to_utc(utc_datetime):
        now_timestamp = time.time()
        offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
        return utc_datetime - offset

    endDate =   datetime.datetime.today()
    # endDate =   datetime.datetime(2019, 8, 24, 19, 0, 0)
    startDate = endDate-datetime.timedelta(days=100)
    print(startDate,endDate)
    endDate = datetime_from_local_to_utc(endDate)
    startDate = datetime_from_local_to_utc(startDate)
    print(startDate,endDate)
    tweets = []
    dates = []
    message = []
    # tmpTweets = api.user_timeline(username)
    
    

    print(len(searched_tweets))
    for tweet in searched_tweets:
        #     tweet.created_at = tweet.created_at + datetime.timedelta(hours=9)
        if tweet.created_at <= endDate and tweet.created_at >= startDate:
            
            if 'retweet_status' in dir(tweet):
                tweet_text = tweet.retweet_status.full_text
            else:
                tweet_text = tweet.full_text
        
            try:
                tweet_text = tweet_text.encode('ascii',errors='ignore').replace('\n',' ').decode('unicode_escape')
            except:
                pass
            
            #append data to the dataframe
            # tweets = pd.read_csv(db_fpath)
            tweet_df = tweet_df.append({'index':str(datetime_from_utc_to_local(tweet.created_at).date()),'tweet':tweet_text,'maker':sym[i]}, ignore_index=True)
            
            tweet_df = tweet_df.drop_duplicates();
tweet_df.to_csv(db_fpath,index=False)

