import datetime
import bs4
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import time


db_fpath='data/chipmaker_google_news_archive_{}.csv'.format(int(time.time()))

if ~os.path.exists(db_fpath):
    handle = open(db_fpath,'w')
    handle.close()

tags = ['NVDA']

#last 7 days
URL = 'https://news.google.com/search?pz=1&cf=all&ned=us&hl=en&tbm=nws&gl=us&q={query}&%20when%3A7d&authuser=0'

article_df = pd.DataFrame(columns=('sym','link','title','body','dttm'))

count=0
for i in range(len(tags)):

    def run(**params):
        print(URL.format(**params))
        response = requests.get(URL.format(**params))
        return response.content, response.status_code

    sym = tags[i]
    content,_=run(query=sym, )


    soup = BeautifulSoup(content, 'html.parser')

    mydivs = soup.findAll("div", {"class": "xrnccd"})

    print('num articles',len(mydivs))
    for div in mydivs:
        article_link = 'https://news.google.com'+div.find("h3",{"class":"ipQwMb ekueJc RD0gLb"}).find('a')['href'][1:]


        article_title = div.find("h3",{"class":"ipQwMb ekueJc RD0gLb"}).string
        
#         if sym in article_title.lower():
        print(article_title)
        article_dttm = div.find("div",{"class":"SVJrMe"}).find('time')['datetime']
        article_dttm = datetime.datetime.strptime(article_dttm,'%Y-%m-%dT%H:%M:%SZ')



        article_synp = div.find("span",{"class":"xBbh9"}).string
        
        article_df.loc[count] = [sym,article_link,article_title,article_synp,article_dttm]

        count+=1
    
    

#             article_raw = requests.get(article_link, timeout=20).content
#             article_raw = BeautifulSoup(article_raw, 'html.parser')
#             article_raw = article_raw.findAll('p',attrs={'class': None})
#             article_text = " ".join(list(map(lambda x: x.text, filter(lambda x: isinstance(x, bs4.Tag), article_raw))))

#             article_df.loc[count] = [sym,article_link,article_title,article_text,article_dttm]
            
#             count+=1
#             time.sleep(1)

article_df.dttm= article_df.dttm.apply(lambda x: datetime.datetime.strftime(x, '%Y-%m-%d %H')) \
                                .apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H'))
                                
article_df['text'] = article_df[['title','body']].apply(lambda x: " ".join(x),axis=1)


article_df.to_csv(db_fpath,index=False)