import json
import pandas as pd
from matplotlib import pyplot as plt
import datetime


#sym = sys.argv[1].split(',')
sym = ['TOMZ','USO']

qry_string = ",".join([s.lower() for s in sym])

count=0
full = pd.DataFrame()
for s in sym[:]:

tmp=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+s+'&apikey=INSERTAPIKEY&datatype=csv')

    if len(tmp)==0:
        print(s+' is empty')
        continue

    tmp = tmp.set_index('timestamp')

    tmp.index = [datetime.datetime.strptime(t,"%Y-%m-%d") for t in tmp.index]
    
    tmp.columns = [s+'_'+c for c in tmp.columns]
    
    if count==0:
        full = tmp[[s+'_close',s+'_volume']]
    else:
        full = full.merge(tmp[[s+'_close',s+'_volume']],left_index=True,right_index=True,how='outer')
    count+=1
    print(full.shape)

full.sort_index(inplace=True)

max_full_date = datetime.datetime.strftime(full.index.max(),'%Y-%m-%d')
stock_names = ",".join(sym)

full.reset_index().to_csv('algo-trading/data/'+qry_string+'_'+max_full_date+'.csv',index=False)


