#KFold_scheme
for tridx,tsidx in kf.split(all_data['target']):
    print(tridx)
    mean = all_data.loc[tsidx,'item_id'].map(all_data.loc[tridx].groupby('item_id').target.mean())
    gc.collect()
    all_data.loc[tsidx,'item_target_enc'] = mean
    gc.collect()

encoded_feature = all_data['item_target_enc'].fillna(0.3343).values
corr = np.corrcoef(all_data['target'].values, encoded_feature)[0][1]
print(corr)

#Leave-one-out_scheme
cnt=all_data.groupby('item_id')['target'].transform('count') 
all_data['item_target_enc'] = all_data.groupby('item_id')['target'].transform('sum')    
all_data['item_target_enc'] = (all_data['item_target_enc'] - all_data['target'])/(cnt-1)
encoded_feature = all_data['item_target_enc'].values
corr = np.corrcoef(all_data['target'].values, encoded_feature)[0][1]
print(corr)


#Smoothing_scheme
global_mean = 0.3343
alpha=100
cnt=all_data.groupby('item_id')['target'].transform('count') 

mean = all_data.groupby('item_id')['target'].transform('mean')
cnt=all_data.groupby('item_id')['target'].transform('count') 

item_target_enc = (mean*cnt + global_mean*alpha)/(cnt+alpha)
gc.collect()
all_data.loc[:,'item_target_enc'] = item_target_enc

encoded_feature = all_data['item_target_enc'].fillna(0.3343).values
corr = np.corrcoef(all_data['target'].values, encoded_feature)[0][1]
print(corr)

#Expanding_mean_scheme
cumsum = all_data.groupby('item_id')['target'].cumsum() - all_data['target']
cumcnt = all_data.groupby('item_id').cumcount()
all_data['item_target_enc'] = cumsum/cumcnt

encoded_feature = all_data['item_target_enc'].fillna(0.3343).values
corr = np.corrcoef(all_data['target'].values, encoded_feature)[0][1]
print(corr)
