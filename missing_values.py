def pandas_isnull_count(col):
    null_count = col.isnull().sum()
    return null_count


def find_potential_nulls(col):
    """
    data = pd.DataFrame()
    data['rand']=np.concatenate([np.random.normal(5,20,(100,)),np.ones(99)])

    data['rand'].value_counts()
    potential_null_col_names = find_potential_nulls(data['rand'])
    """
    
    null_count = pandas_isnull_count(col)
    
    if null_count==0:
        uniq_vals,uniq_count = np.unique(col.values,return_counts=True)
        #if the number of unique values is >30 and a category represents more than 20% of the data
        #this could be an indication of a missing value

        msk = len(uniq_vals)>30 and uniq_count/col.shape[0]>0.20
        return uniq_vals[msk]
        
        

