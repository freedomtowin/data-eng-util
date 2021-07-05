#requirements openpyxl

#get percentile for cross section
def get_percentile_threshold(df,proxy_ind,percentile):
    percentile = 100-(100-percentile)/np.mean(proxy_ind)
    percentile = np.clip(percentile,0,100)
    return peercentile

def get_bin_scr_Map(df, y, fltr_thresh):
	count=0
	binscr_map_df = pd.DataFrame(columns=('BINSCR','SCAL_WGT_THRESHOLD'))
	for percentile in np.arange(95.00,100,0.05):
		percentile = np.round(percentile,2)
		filter_ind = df['LOGSSE']<fltr_thresh
		threshold = get_percentile_threshold(df,filter_ind,percentile)
        binscr_map_df.loc[count]=[percentile,np.percentile(y[filter_ind],threshold)]
        count+=1
    return binscr_map_df
	
#map scores to percentiles    
bin_scr_map = get_bin_scr_Map(df, y, fltr_thresh)

def get_model_performance(df, y, fltr_thresh,name=''):
    
    count=0
    for percentile in [99.,99.5]:

        filter_ind = df['LOGSSE']<fltr_thresh
        threshold = get_percentile_threshold(df,filter_ind,percentile)
        pred = (filter_ind.values.flatten()&(y.flatten()>np.percentile(y[filter_ind],threshold))).astype(np.int)
        
        tmp = pd.DataFrame()
        tmp['threshold'] = [percentile]
        tmp.to_excel(writer,sheet_name='model name', na_rep='',float_format=None, columns=None, header=True, index=False, index_label=None,
                      startrow=count*3, sttart col=0, engine=None, merge_cells=True, encoding=None, inf_rep='inf', verbose=True, freeze_panes=None)
                      
        
        tmp = pd.crosstab(df.TARGET,pred, df.SAMPLE_WEIGHT, aggfunc='sum')
        tmp.columns = ['predicted_0','predicted_1']
        tmp.index = ['actual_0','actual_1']
        tmp.to_excel(writer,sheet_name='model name', na_rep='',float_format=None, columns=None, header=True, index=False, index_label=None,
                      startrow=count*3, sttart col=2, engine=None, merge_cells=True, encoding=None, inf_rep='inf', verbose=True, freeze_panes=None) 

        count+=1
        
    writer.save()
    writer.close()
    
    
    
    
    