import json
import pandas as pd
import numpy as np
import datetime




db_fpath='data/chipmaker_stock_price_archive_{}.csv'.format(int(time.time()))

if ~os.path.exists(db_fpath):
    handle = open(db_fpath,'w')
    handle.close()
    

sym = ['NVDA','XLNX','AMD','LSCC','INTC']

qry_string = ",".join([s.lower() for s in sym])

count=0
full = pd.DataFrame()
for s in sym[:]:
        
    tmp=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=60min&symbol='+s+'&apikey=VS5EP0GAR3RZDMUB&datatype=csv')

    if len(tmp)==0:
        print(s+' is empty')
        continue

    tmp = tmp.set_index('timestamp')

    tmp.index = [datetime.datetime.strptime(t,"%Y-%m-%d %H:%M:%S") for t in tmp.index]
    
    tmp.columns = [s+'_'+c for c in tmp.columns]

    if count==0:
        full = tmp[[s+'_close',s+'_volume']]
    else:
        full = full.merge(tmp[[s+'_close',s+'_volume']],left_index=True,right_index=True,how='outer')
    count+=1
    
full.reset_index().to_csv(db_fpath,index=False)