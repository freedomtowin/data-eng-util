import re
from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd
import math
import requests
import datetime
import time
import subprocess
import tweepy
# from multiprocessing import Process, Pool
# module imports
# from src.extract import Extract
# from src.listing_parser import ListingParser
# from src.utils import Utils
#from 
import os

class ButtStock:
    """ Search class is responsible for parsing a For-Sale search in craigslist """

    def __init__(self, **kwargs):
        #self.__params = {}
        #self.__total = (0,0,0)
        #self.__search_type = None
        self.__symbol = kwargs['symbol']
        self.__twitter_handle = kwargs['twitter_handle']
        # super().__init__(kwargs['city'], kwargs['search_type'], kwargs['vendor'])

    def get_params(self):
        """ get search parameters """
        return self.__params

    def set_params(self, **params):
        """ set search parameters """
        self.__params = params

    def get_search_type(self):
        return self.__search_type

    def get_symbol(self):
        return self.__symbol
        
    def get_twitter_handle(self):
        return self.__twitter_handle
        
    def get_stock_prices(self):
            
        ALPHA_VANTAGE_KEY = os.environ.get('ALPHA_VANTAGE_KEY')
        
        full = pd.DataFrame()
        sym = self.get_symbol()
                
        tmp=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=60min&symbol='+sym+'&apikey='+ALPHA_VANTAGE_KEY+'&datatype=csv')

        # if len(tmp)==0:
            # print(s+' is empty')
            # continue

        tmp = tmp.set_index('timestamp')

        tmp['time'] = [datetime.datetime.strftime(datetime.datetime.strptime(t,"%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S") for t in tmp.index]
        
        tmp['sym'] = sym.lower()
        
        tmp['source'] = 'alpha_vantage_key'
        
        return tmp
        
    def get_google_news(self):
    
        def run_query(URL,**params):
            print(URL.format(**params))
            response = requests.get(URL.format(**params))
            return response.content

        def tag_visible(element):
            if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                return False
            if isinstance(element, Comment):
                return False
            return True


        def text_from_html(body):
            soup = BeautifulSoup(body, 'html.parser')
            texts = soup.findAll(text=True)
            visible_texts = filter(tag_visible, texts)  
            return u" ".join(t.strip() for t in visible_texts)
        
        URL = 'https://news.google.com/search?pz=1&cf=all&ned=us&hl=en&tbm=nws&gl=us&q={query}&%20when%3A7d&authuser=0'

        article_df = pd.DataFrame(columns=('sym','link','title','body','time'))
        sym = self.get_symbol()
        
        count=0
        
        endDate =   datetime.datetime.today()
        # endDate =   datetime.datetime(2019, 8, 24, 19, 0, 0)
        startDate = endDate-datetime.timedelta(days=3)
        
        content=run_query(URL,query=sym, )

        soup = BeautifulSoup(content, 'html.parser')

        mydivs = soup.findAll("div", {"class": "xrnccd"})

        print('num articles',len(mydivs))
        for div in mydivs:
            
            article_dttm = div.find("div",{"class":"SVJrMe"}).find('time')['datetime']
            article_dttm = datetime.datetime.strptime(article_dttm,'%Y-%m-%dT%H:%M:%SZ')
            
            article_link = 'https://news.google.com'+div.find("h3",{"class":"ipQwMb ekueJc RD0gLb"}).find('a')['href'][1:]

            article_title = div.find("h3",{"class":"ipQwMb ekueJc RD0gLb"}).string
            
            if article_dttm <= endDate and article_dttm >= startDate:

                try:
                    article_synp = text_from_html(requests.get(article_link, timeout=5).content)
                except Exception as e:
                    print(e)
                    continue
                    
                if sym not in article_synp:
                    continue
                    
                article_df.loc[count] = [sym,article_link,article_title,article_synp,article_dttm]

                count+=1

        article_df['time']= article_df.time.apply(lambda x: datetime.datetime.strftime(x, '%Y-%m-%d %H'))
        
        article_df['text'] = article_df[['title','body']].apply(lambda x: " ".join(x),axis=1)

        article_df['source'] = 'google_news'

        return article_df
        
    def get_tweets(self):
    
    
        TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
        TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
        TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
        TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')    
    
        # TWITTER_CONSUMER_KEY = self.get_twitter_consumer_key()
		# TWITTER_CONSUMER_SECRET = self.get_twitter_consumer_secret()
		# TWITTER_ACCESS_TOKEN = self.get_twitter_access_token()
		# TWITTER_ACCESS_TOKEN_SECRET = self.get_twitter_access_token_secret()
    
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)
        
        sym = self.get_symbol()
        twitter_handle = self.get_twitter_handle()
        

        query = 'from:'+twitter_handle
        max_tweets = 100
        searched_tweets = [status for status in tweepy.Cursor(api.search, q=query, tweet_mode='extended').items(max_tweets)]


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
        startDate = endDate-datetime.timedelta(days=3)
        endDate = datetime_from_local_to_utc(endDate)
        startDate = datetime_from_local_to_utc(startDate)

        tweets = []
        dates = []
        message = []
        # tmpTweets = api.user_timeline(username)
        
        
        tweet_df = pd.DataFrame(columns=('time','tweet','sym'))
        
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
                tweet_df = tweet_df.append({'time':str(datetime_from_utc_to_local(tweet.created_at).date()),'tweet':tweet_text,'sym':sym}, ignore_index=True)
                
                tweet_df = tweet_df.drop_duplicates();
                
        tweet_df['source'] = 'twitter'
        return tweet_df


    # def soupify(self, params):
        # """ Creates bs4 formatted soup from html response """
        # (response, search_type, city) = self.extract_search(**params)
        # self.__search_type = search_type
        # self.__city = city
        # soup = BeautifulSoup(response.text, 'html.parser')
        # self.__get_totals(soup)
        # return soup
"""
    def extract_all_postings(self, first_page_only=False, depth=2, get_body=False):
        #Extract and parse all data from postings according to search
        first_group = self.soupify(self.__params)
        if sum(self.__total) == 0:
            yield None
        # scraping first page of results
        if first_page_only:
            # extract data from first page of search results
            yield self.__parse_listings(0, first_group, depth, get_body)
        # scraping all result pages
        else:
            # calculate search groups
            ranges = self.__total[2]/self.__total[1]
            groups = math.ceil(ranges) - 1
            # totals
            group_total = self.__total[1]
            search_total = self.__total[2]
            # set list of search group amounts for url
            s_num = [0] + [group_total * (i+1) if group_total * (i+1) <= search_total else search_total - 1 for i in range(groups)]
            for i in s_num:
                yield self.__parse_listings(i,first_group,depth,get_body)

    def __get_totals(self, soup):
        #Get totals from search results
        pnum_span = soup.select_one('.pagenum')
        if pnum_span.text != 'no results':
            range_1 = int(pnum_span.span.select_one('.rangeFrom').text)
            range_2 = int(pnum_span.span.select_one('.rangeTo').text)
            total = int(pnum_span.select_one('.totalcount').text)
            self.__total = (range_1, range_2, total)
            self.__params['s'] = range_2
            # check for limit
            self.__limit = self.__check_limit(soup)
        return self.__total


    def __check_limit(self, html):
        #Check if results are limited and set last posting id if applicable
        limit = html.find('ul',class_='rows')
        h4 = limit.h4
        if h4:
            l = limit.h4.find_previous_sibling('li')
            return l['data-pid']
        else:
            return None
 
    def __get_posting_hrefs(self, soup):
        #Get all posting urls from search results
        urls = []
        links = soup.findAll('a', class_='result-title hdrlnk')
        for a in links:
            urls.append(a['href'])
            if self.__limit and a['data-id'] == self.__limit:
                break
        return urls


    def __parse_listings(self, search_num, html, depth, get_body):
        #Parse listing info from search results
        self.__params['s'] = search_num
        search_results = self.soupify(self.__params) if search_num > 0 else html
        make_model = self.__params['auto_make_model'] if 'auto_make_model' in self.__params else None
        if depth == 1:
            listings = search_results.find_all(attrs={'class': 'result-row'})
            posts = []
            for li in listings:
                info = self.parse_listing_info(li, make_model)
                posts.append(info)
                if self.__limit and info['posting_id'] == self.__limit:
                    break
        elif depth == 2:
            # search by urls --> will not be using values from post
            urls = self.__get_posting_hrefs(search_results)   
            p = Pool(20)
            urls = [(u, make_model, get_body) for u in urls]
            posts = p.starmap(self.parse_individual_post, urls)
            p.terminate()
            p.join()
        return posts
 """