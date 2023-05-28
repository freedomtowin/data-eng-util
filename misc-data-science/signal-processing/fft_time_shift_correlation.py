def time_correlation(ts1,ts2):
    
    cross = np.fft.fft(ts1.flatten())*np.conjugate(np.fft.fft(ts2.flatten()))
    cc = np.absolute(np.fft.ifft(cross))
    half =  round(len(ts2)/2+0.5,0)
    g = np.concatenate([np.arange(0,half),np.arange(half,len(ts2))-len(ts2)])
    shift = [(val,i) for i,val in zip(g,cc.flatten()) if val==np.max(cc.flatten())]
    return shift