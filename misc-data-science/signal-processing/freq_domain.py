def get_frequency_domain(signal):
    N = len(signal)
    yf = np.fft.fft(signal)
    freq= np.fft.fftfreq(len(yf))
    return np.column_stack((freq[:N//2],yf[:N//2]))  
