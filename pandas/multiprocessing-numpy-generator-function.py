from multiprocessing import Pool
import numpy as np

def process_array(X):
    return X

pool = Pool(6)
n = X.shape[0]

def generator():
    for i in range(n):
        yield X[i:i+1]
    print("generator done")

map_result = pool.map(process_array,generator())

result = np.vstack(map_result)
