"""
create a coordinate matrix between two id fields
"""

#test is a pandas dataframe
coords = np.vstack([test[['FirstId','SecondId']].values,test[['SecondId','FirstId']].values])

coords = pd.DataFrame(coords,columns = ('FirstId','SecondId'))
coords = coords.drop_duplicates()

maxId = np.maximum(coords.FirstId.max(),coords.SecondId.max())

data = np.ones(coords.shape[0])

import scipy
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.coo_matrix.html
#coo_matrix((data, (i, j)), [shape=(M, N)])
#to construct from three arrays:
#data[:] the entries of the matrix, in any order
#i[:] the row indices of the matrix entries
#j[:] the column indices of the matrix entries

inc_mat = scipy.sparse.coo_matrix((data, (coords.FirstId.values.ravel(), coords.SecondId.values.ravel()))
                        ,(maxId+1, maxId+1), dtype=np.int8 ) 
                        

rows_FirstId   = inc_mat[test.FirstId.values]
rows_SecondId  = inc_mat[test.SecondId.values]

#dot product to get the similarity between connections between ids
f = rows_FirstId.multiply(rows_SecondId).sum(axis=1)

val,cnts = np.unique(f.A,return_counts=True)

"""
expand out rows for multiple id columns and a time-based index column
"""

index_cols = ['shop_id', 'item_id', 'date_block_num']

# For every month we create a grid from all shops/items combinations for the date_block_num
grid = []
for block_num in sales['date_block_num'].unique():
    cur_shops = sales.loc[sales['date_block_num'] == block_num, 'shop_id'].unique()
    cur_items = sales.loc[sales['date_block_num'] == block_num, 'item_id'].unique()
    grid.append(np.array(list(product(*[cur_shops, cur_items, [block_num]])),dtype='int32'))

# Turn the grid into a dataframe, it will have all three of the id columns
grid = pd.DataFrame(np.vstack(grid), columns = index_cols,dtype=np.int32)