def trend_decomp(sig,N):
    part = int(len(sig)/N)
    i=0
    j=0
    slopes = np.zeros(N+1)
    intercepts = np.zeros(N+1)
    while i<len(sig):
        end_i = i+part
        if end_i>len(sig):
            end_i = len(sig)
        sig_part = sig[i:end_i]
        x = np.column_stack((np.ones((len(sig_part),1)),np.arange(0,len(sig_part))))
        A=x.T.dot(x)
        b=x.T.dot(sig_part)
        z = np.linalg.solve(A,b)
        slopes[j] = z[1]
        intercepts[j] = z[0]
        i=i+part
        j+=1

    return intercepts,slopes
        
N = 15
bintercepts = np.zeros((df_pivot.values.T.shape[0],N+1))
bslopes = np.zeros((df_pivot.values.T.shape[0],N+1))
for i in range(df_pivot.values.T.shape[0]):
    bintercepts[i],bslopes[i] = trend_decomp(df_pivot.values.T[i],N)