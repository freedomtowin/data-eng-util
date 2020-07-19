
import numpy

import ipyparallel as ipp
from ipyparallel import Client
rc = Client(profile='default')
dview = rc[:]


# dview.block = False

# rc.debug = True
with dview.sync_imports():
    import numpy
    import gc
    
#however many core you started 
#dview.target = [1..ncores]
num_cores = len(dview.targets)
    
dview.execute('np=numpy')
dview.execute('np.mkl.set_num_threads(1)')

import numpy as np
import pandas as pd

#create dataset
data = np.random.uniform(-10,10,size=(5000000,3))
df = pd.DataFrame(data,columns=('x1','x2','x3'))

df_split = np.array_split(df, 6, axis=0)

#load the dataframe chunk into the core
for i in dview.targets:
    print('chunk:',i,'df shape:',df_split[i].shape)
    rc[i]['df'] = df_split[i]
        
    
#create a reference to each dataframe
#this allows you do pass the reference instead of the data
rdf = [ipp.Reference('df') for i in range(num_cores)]

def map_nunique(df):
    return df.nunique()

def reduce_nunique(x):
    return pd.concat(x).groupby(level=0).sum()
    
%%time
reduce_nunique(dview.map_sync(map_nunique,rdf))

%%time
df.nunique()

def map_nearest_neighbors(df,qry,k=10):
    euclid = np.sum((df.values-qry)**2,axis=1)
    sort_dist = np.argsort(euclid)
    return df.iloc[sort_dist[:10]]

def reduce_nearest_neighbors(df,qry):
    subset_df = pd.concat(df,axis=0)
    euclid = np.sum((subset_df.values-qry)**2,axis=1)
    sort_dist = np.argsort(euclid)
    return subset_df.iloc[sort_dist[:10]]
    
%%time
qry = np.array([[0,0,0]])
rqry = [qry for _ in range(num_cores)]
parallel_result = dview.map_sync(map_nearest_neighbors,rdf,rqry)
reduce_nearest_neighbors(parallel_result,qry)

%%time
qry = np.array([[0,0,0]])
map_nearest_neighbors(df,qry)
