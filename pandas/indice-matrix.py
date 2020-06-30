coords = np.vstack([test[['FirstId','SecondId']].values,test[['SecondId','FirstId']].values])

coords = pd.DataFrame(coords,columns = ('FirstId','SecondId'))
coords = coords.drop_duplicates()

maxId = np.maximum(coords.FirstId.max(),coords.SecondId.max())

data = np.ones(coords.shape[0])

import scipy

inc_mat = scipy.sparse.coo_matrix((data, (coords.FirstId.values.ravel(), coords.SecondId.values.ravel()))
                        ,(maxId+1, maxId+1), dtype=np.int8 ) 
                        

rows_FirstId   = inc_mat[test.FirstId.values]
rows_SecondId  = inc_mat[test.SecondId.values]

f = rows_FirstId.multiply(rows_SecondId).sum(axis=1)

val,cnts = np.unique(f.A,return_counts=True)

