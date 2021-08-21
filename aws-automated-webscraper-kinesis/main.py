import os, json, sys
import pandas as pd
import datetime
import time
from src.search import ButtStock
from src.utils import KinesisDataClient
import io
import boto3


data_stream = KinesisDataClient('kinesis','us-east-1')

try:
    # if os.environ.get('ENV') in ['dev', 'local']:
        # from dotenv import load_dotenv
        # load_dotenv()

    ##get search params from environment variables
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket='rk-stock-data-s3', Key='stock_scrape_list.csv')
    scrape_list = pd.read_csv(io.BytesIO(obj['Body'].read()))
    

    # TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
    # TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
    # TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    # TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')    
    
    # city = os.environ.get('SEARCH_CITY_URL')
    # if city is None:
        # city = os.environ.get('SEARCH_CITY')
    # make_model = os.environ.get('MAKE_MODEL')
    # depth = os.environ.get('SEARCH_DEPTH')
    # get_body = os.environ.get('GET_BODY')

    # if all(v is None for v in [search_type, vendor, city, depth, get_body]):
        # print('Necessary environment variables missing... Clean exit')
        # exit(0)
    # else:
        # depth = int(depth)
        # get_body = bool(get_body)


except Exception as err:
    print(err)
    print("Error loading environment variables...")
    print("Exiting scraper... Clean exit")
    exit(0)

def main():

    for symbol, twitter_handle in scrape_list.values:

        #try:
            # initialize search class with parameters
        bt = ButtStock(symbol=symbol, twitter_handle=twitter_handle)
        
        stock_price = bt.get_stock_prices()
        data_stream.send_kinesis('rk-stock-price-stream',1,stock_price)
        
        stock_news = bt.get_google_news()
        data_stream.send_kinesis('rk-stock-news-stream',1,stock_news)
        
        stock_tweets = bt.get_tweets() 
        data_stream.send_kinesis('rk-stock-tweet-stream',1,stock_tweets)               

    # except Exception as err:
        # print("Error running scraper...")
        # print("Exiting scraper with exit code 0...")
        # print(err)
        # exit(0)


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, TypeError, NameError) as err:
        print(err)
        print('Failed to execute main function')
        exit(0)