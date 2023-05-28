def autocorrelation(x1,x2):
    result = np.correlate(x1, x2, mode='same')
    result = result[result.size//4:3*result.size//4]
    result = result[result.size//2:]
    return result