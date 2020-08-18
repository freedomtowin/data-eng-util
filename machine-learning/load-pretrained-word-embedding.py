
#load GloVe
def loadGloveModel(gloveFile):
    f = open(gloveFile,'rb')
    model = {}
    for line in f:
        splitline = line.split()
        word = splitline[0].decode('utf-8')
        if word!=word.lower():
            continue
        embedding = [float(val) for val in splitline[1:]]
        model[word] = embedding
    return model

#https://nlp.stanford.edu/projects/glove/
glv = loadGloveModel('glove/glove.6B.50d.txt')


#FastText
"""
# import io

# def load_vectors(fname):
#     fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
#     n, d = map(int, fin.readline().split())
#     data = {}
#     for line in fin:
#         tokens = line.rstrip().split(' ')
#         word = tokens[0]
        
#         if word!=word.lower() and len(word)>1:
#             continue
#         data[tokens[0]] = list(map(float, tokens[1:]))
        
#     return data
#https://fasttext.cc/docs/en/pretrained-vectors.html
# russion_w2v_file = os.path.join(DATA_FOLDER, 'wiki.ru.vec')
# russion_w2v = load_vectors(russion_w2v_file)
"""


import pandas as pd
import numpy as np
items = ['dog cat  ',
    'america   china',
    '  caffiene nicotine']
item_df = pd.DataFrame()

item_df['item'] = items

#removing un-necessary spacs
def remove_dup_spaces(x):
    lenx = len(x)
    count = 0
    spaces = ""
    for i in x:
        if i == " ":
            count+=1
            spaces+=" "
        elif i != " " and count > 0:
            x = x.replace(spaces," ")
            count = 0
            spaces = ""
    return x.strip()

item_df.item = item_df.item.apply(lambda x: remove_dup_spaces(x))

#get the output embedding layer
import re
embed = np.zeros((item_df.shape[0],50))

for n in range(item_df.shape[0]):
    item = item_df.loc[n,'item']
    
    if item is None:
        continue
    
    item = re.sub('[^a-zA-Z \n\.]',' ',item.lower())
    grams = item.split(' ')
    gram_cnt = len(grams)
    for word in grams:
        
        if word in glv.keys():
            for i in range(0,50):
                embed[n,i] = embed[n,i] + (glv[word][i])/gram_cnt
              
    norm = np.sum(embed[n]**2)
    
    if norm==0:
        continue
        
    embed[n] = embed[n]/np.sqrt(norm)
