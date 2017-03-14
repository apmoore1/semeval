# How to use the word vectors in Python

import gensim

word_model = gensim.models.Word2Vec.load('all_fin_model_lower')

word_model.most_similar('tesco')

Above shows an example of how to load the word2vec models using gensim in Python. To 
see the full API details go to this [page](https://radimrehurek.com/gensim/models/word2vec.html)
