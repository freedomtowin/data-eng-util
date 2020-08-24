mean_enc_cols = ['shop_id', 'item_id', 'item_category_id', 'super_item_category_id']

def kfold_mean_enc(df,gb_col,target_name='item_cnt_month'):
    #KFold_scheme
    kf = model_selection.KFold(5)
    
    global_mean = df[target_name].mean()
    
    gb_col_rename = gb_col+'_kfold_target_enc'
    
    mean_enc_df = pd.DataFrame(index=df.index)
    mean_enc_df[target_name] = df[target_name]
    
    for tridx,tsidx in kf.split(df[target_name]):
        fkold_mean = df.loc[tsidx,gb_col].map(df.loc[tridx].groupby(gb_col)[target_name].mean())
        mean_enc_df.loc[tsidx,gb_col_rename] = fkold_mean
        gc.collect()

    encoded_feature = mean_enc_df[gb_col_rename].fillna(global_mean)
    corr = np.corrcoef(mean_enc_df[target_name].values, encoded_feature.values)[0][1]
    print('kfold {} mean encoding correlation {}'.format(gb_col,corr))
    return encoded_feature


def loo_mean_enc(df,gb_col,target_name='item_cnt_month'):
    #KFold_scheme
    kf = model_selection.KFold(5)
    
    global_mean = df[target_name].mean()
    
    gb_col_rename = gb_col+'_loo_target_enc'
    
    mean_enc_df = pd.DataFrame(index=df.index)
    mean_enc_df[target_name] = df[target_name]
    
    
    cnt=df.groupby(gb_col)[target_name].transform('count')
    mean_enc_df[gb_col_rename] = df.groupby(gb_col)[target_name].transform('sum')
    mean_enc_df[gb_col_rename] = (mean_enc_df[gb_col_rename] - mean_enc_df[target_name])/(cnt-1)
    encoded_feature = mean_enc_df[gb_col_rename]
    gc.collect()
    
    corr = np.corrcoef(mean_enc_df[target_name].values, encoded_feature.values)[0][1]
    print('kfold {} loo encoding correlation {}'.format(gb_col_rename,corr))
    return encoded_feature

def smoothing_mean_enc(df,gb_col,alpha=100,target_name='item_cnt_month'):
    #KFold_scheme
    kf = model_selection.KFold(5)
    
    global_mean = df[target_name].mean()
    
    gb_col_rename = gb_col+'_smooth_target_enc'
    
    mean_enc_df = pd.DataFrame(index=df.index)
    mean_enc_df[target_name] = df[target_name]
    
    
    gb_cnt=df.groupby(gb_col)[target_name].transform('count')

    gb_mean = df.groupby(gb_col)[target_name].transform('mean')

    mean_target_enc = (gb_mean*gb_cnt + global_mean*alpha)/(gb_cnt+alpha)
    
    mean_enc_df[gb_col_rename] = mean_target_enc
    gc.collect()

    encoded_feature = mean_enc_df[gb_col_rename].fillna(global_mean)
    corr = np.corrcoef(mean_enc_df[target_name].values, encoded_feature.values)[0][1]
    print('kfold {} smoothing encoding correlation {} alpha {}'.format(gb_col_rename,corr,alpha))
    return encoded_feature

def expanding_mean_enc(df,gb_col,target_name='item_cnt_month'):
    #KFold_scheme
    kf = model_selection.KFold(5)
    
    global_mean = df[target_name].mean()
    
    gb_col_rename = gb_col+'_expanding_target_enc'
    
    mean_enc_df = pd.DataFrame(index=df.index)
    mean_enc_df[target_name] = df[target_name]
    
    
    cumsum = df.groupby(gb_col)[target_name].cumsum() - df[target_name]
    cumcnt = df.groupby(gb_col).cumcount()
    mean_enc_df[gb_col_rename] = cumsum/cumcnt

    encoded_feature = mean_enc_df[gb_col_rename].fillna(global_mean)
    
    corr = np.corrcoef(mean_enc_df[target_name].values, encoded_feature.values)[0][1]
    print('kfold {} expanding encoding correlation {}'.format(gb_col_rename,corr))
    return encoded_feature

"""
#The expanding mean schema had the highest correlation to the item count month

mean_enc_result = list(map(lambda x: kfold_mean_enc(train,x),mean_enc_cols))
print()
mean_enc_result += list(map(lambda x: loo_mean_enc(train,x),mean_enc_cols))
print()
mean_enc_result += list(map(lambda x: smoothing_mean_enc(train,x,alpha=10),mean_enc_cols))
print()
mean_enc_result += list(map(lambda x: expanding_mean_enc(train,x),mean_enc_cols))
"""

#
mean_enc_result = list(map(lambda x: expanding_mean_enc(train,x),mean_enc_cols))
mean_enc_result = pd.concat(mean_enc_result,axis=1)
