# Utilities For Data Engineering and Machine Learning

This repository is a compilation of script I have used in the past. All code is either original, modified version of someone else's code, or from an educational source. Credit will be given to any direct copy of someone else's work.

# Data Processing

coordinate-matrix-ops.py - create a sparse matrix of edges (connections) between two ID columns, create an index column dataframe for multiple id fields

ipyparallel-pandas.py - parallelize pandas dataframe with ipyparallel

alphavantage-data-api.py - download multiple daily stock elements from the alphavantage api into a pandas dataframe

twitter-data-api.py - download twitter feed from specific authors into a pandas dataframe

multiprocessing-numpy-generator-function.py- process a numpy array in parallel with a generator function 

type-casting-pandas.py - functions to pre-processing types in pandas dataframe

cramers-v.py- Cramer's V, measure of association between nominal variables.


# Machine Learning

mean-encoding-regularization.py- regularization strategies for mean-encoded categorical variables

tf-gradient-tape-example.py - tensorflow backend to create custom training workflows with tensorflow datasets 

tf-gradient-importance.py- calculates the gradients of the output with respect to the input, feature importance

# Natural Language Processing

load-pretrained-glove.py - load GloVe (NLP) pre-trained word embedding features, load FastText Wiki word embeddings

text_preprocessing_lstm.py - Text tokenization, sequence, and padding for LSTM modeling using TensorFlow

# Computer Vision

[video-to-frames.py]


# Signal Processing

phase-corr-shift.py - get the phase shift between 1-d and 2-d matrices using the phase correlation


# Geospatial

bokeh-geomap.py - read a .shp file with geopandas and plot it with bokeh, finds census tract for location 

maxbox-geoencoding.py - geoencoding using the MapBox API

