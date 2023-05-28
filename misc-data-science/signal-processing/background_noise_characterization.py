def background_noise(sig,W):
    sig = sig[:-4]-np.convolve(sig,np.ones(5)/5,mode='valid')
    sig = sig-np.min(sig)+1e-10
    N = len(sig)
    f = np.zeros(W)
    for n in range(0,5000):
        i = np.random.randint(0,N-W)
        f = f*(n)/(n+1) + np.fft.fftshift(np.fft.fft(sig[i:i+W])*1/(n+1))
    f = np.absolute(np.fft.ifft(f))
    limiter = np.max(f)
    f = np.log(f+limiter*0.01) - np.log(limiter*0.01)
    return f
    
W = 15
bnoise = np.zeros((df_pivot.values.T.shape[0],W))
for i in range(df_pivot.values.T.shape[0]):
    bnoise[i] = background_noise(df_pivot.values.T[i],W)